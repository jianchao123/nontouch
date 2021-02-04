# coding:utf-8
from decimal import Decimal
from datetime import timedelta
from datetime import datetime
from datetime import date
from collections import defaultdict
from timer import db


class ActivitiesTimer(object):

    @db.transaction(is_commit=True)
    def change_activity_status(self, mysql_cur):
        """
        <修改优惠券活动状态>
        1.当前活动状态为未开始,但分发时间已开始,修改状态为(2)
        2.当前活动状态为活动中,但分发时间已结束,修改状态为(3)
        """
        cur_time = datetime.now()
        mysql_db = db.MysqlDbUtil(mysql_cur)

        coupon_type_sql = "SELECT `id`,`give_out_begin_time`," \
                          "`give_out_end_time`, `use_begin_time`," \
                          "`use_end_time`,`status` FROM `coupon_type` "
        volume_sql = "SELECT COUNT(`id`) FROM `coupon` WHERE " \
                     "`type_id`={} AND `status`=1"

        result = mysql_db.query(coupon_type_sql)
        for row in result:
            pk = row[0]
            give_out_begin_time = row[1]
            give_out_end_time = row[2]

            status = row[5]

            d = defaultdict()
            # 未开始状态 (影响活动状态的只有分发时间和活动优惠券数量)
            if status == 1:
                if give_out_begin_time < cur_time < give_out_end_time:
                    d["`status`"] = 2
                    d["`is_online`"] = 1
            # 活动中状态
            elif status == 2:
                if cur_time > give_out_end_time:
                    d["`status`"] = 3
                else:
                    volume_result = mysql_db.get(volume_sql.format(pk))
                    print volume_result
                    volume = volume_result[0] if volume_result else 0
                    # 数量发完,修改状态为结束
                    if not volume:
                        d["`status`"] = 3
            if d:
                d["`id`"] = pk
                mysql_db.update(d, table_name='`coupon_type`')

    @db.transaction(is_commit=True)
    def change_coupe_status(self, mysql_cur):
        """
        <已分配的优惠券状态修改>
        1.已分配并且未使用的优惠券过期(2),修改状态为已过期(4)
        """
        # 1.已经领取并且未使用的优惠券,如果已到使用截止时间,修改状态为已过期
        user_coupe_sql = "SELECT uc.`id`,c.`id`,c.`use_begin_time`," \
                         "c.`use_end_time` FROM `user_coupe` as uc " \
                         "INNER JOIN `coupon` as c ON uc.coupon_id=c.id " \
                         "WHERE c.`status`=2"
        mysql_db = db.MysqlDbUtil(mysql_cur)
        result = mysql_db.query(user_coupe_sql)
        cur_time = datetime.now()
        for row in result:
            coupon_id = row[1]
            use_end_time = row[3]
            if cur_time > use_end_time:
                mysql_db.update({"`id`": coupon_id, "`status`": 4},
                                table_name="`coupon`")

    @db.transaction(is_commit=True)
    def update_coupon_data(self, mysql_cur):
        """
        <更新优惠券活动相关的数据>
        1.已发放量 2.已使用量
        """
        coupon_type_sql = "SELECT `id`,`volume` FROM `coupon_type` "
        coupon_sql = "SELECT COUNT(`id`) FROM `coupon` WHERE " \
                     "`type_id`={} AND `status` in ({})"
        mysql_db = db.MysqlDbUtil(mysql_cur)
        result = mysql_db.query(coupon_type_sql)
        for row in result:
            coupon_type_pk = row[0]
            total_volume = row[1]

            # 已发放量(已领取)
            sql = coupon_sql.format(coupon_type_pk, "2,3,4")
            result = mysql_db.get(sql)
            give_out_voluem = result[0] if result else 0
            d = defaultdict()
            d["`id`"] = coupon_type_pk
            if give_out_voluem:
                d["`residue_volume`"] = total_volume - give_out_voluem

            # 已使用量
            sql = coupon_sql.format(coupon_type_pk, "3")
            result = mysql_db.get(sql)
            has_been_used_volume = result[0] if result else 0
            if has_been_used_volume:
                d["`has_been_used_volume`"] = has_been_used_volume
            if give_out_voluem or has_been_used_volume:
                mysql_db.update(d, table_name="coupon_type")

    @staticmethod
    def insert_user_coupe(mysql_db, coupon_ids, user_id,
                          ct_use_begin_time, ct_use_end_time):
        for coupon_id in coupon_ids:
            d = {
                "`user_id`": user_id,
                "`coupon_id`": coupon_id,
                "`get_time`": 'now()'
            }
            mysql_db.insert(d, table_name="`user_coupe`")
            use_begin_time = "STR_TO_DATE('{}', '%Y-%m-%d %H:%i:%s')".format(
                ct_use_begin_time.strftime("%Y-%m-%d %H:%M:%S"))
            use_end_time = "STR_TO_DATE('{}', '%Y-%m-%d %H:%i:%s')".format(
                ct_use_end_time.strftime("%Y-%m-%d %H:%M:%S"))
            d = {
                "`id`": coupon_id,
                "`status`": 2,
                "`use_begin_time`": use_begin_time,
                "`use_end_time`": use_end_time
            }
            mysql_db.update(d, table_name="`coupon`")

    @db.transaction(is_commit=True)
    def invited_users_give_coupon(self, mysql_cur):
        """
        <邀请用户送优惠券>
        该定时器启动之前要先手动增加活动
        """
        rds_conn = db.rds_conn
        mysql_db = db.MysqlDbUtil(mysql_cur)
        coupon_type_sql = "SELECT `id`,`face_value`,`use_begin_time`," \
                          "`use_end_time` FROM `coupon_type` " \
                          "WHERE `condition`=3"
        user_sql = "SELECT `id` FROM `user_profile` WHERE `mobile`={}"
        sql = "SELECT `id` FROM `coupon` WHERE " \
              "`type_id`={} and `status`=1 LIMIT {}"
        mobile_str = rds_conn.lpop("SHARE_PRESENT_COUPE")
        while mobile_str:
            mobile_arr = mobile_str.split(":")
            new_user = mobile_arr[0]
            invite_user = mobile_arr[1]
            print(u"自动赠送优惠券-{}".format(mobile_str))
            new_user = mysql_db.get(user_sql.format(new_user))[0]
            invite_user = mysql_db.get(user_sql.format(invite_user))[0]

            coupon_types = mysql_db.query(coupon_type_sql)
            for coupon_type in coupon_types:
                new_user_coupon_ids = None
                invite_user_coupon_ids = None

                ct_id = coupon_type[0]
                ct_face_value = coupon_type[1]
                ct_use_begin_time = coupon_type[2]
                ct_use_end_time = coupon_type[3]

                if ct_face_value == Decimal(str(1.5)):
                    result = mysql_db.query(sql.format(ct_id, 2))
                    coupon_ids = [row[0] for row in result]
                    new_user_coupon_ids = coupon_ids[:1]
                    invite_user_coupon_ids = coupon_ids[1:]

                if ct_face_value == Decimal(str(0.8)):
                    result = mysql_db.query(sql.format(ct_id, 2))
                    coupon_ids = [row[0] for row in result]
                    new_user_coupon_ids = coupon_ids[:1]
                    invite_user_coupon_ids = coupon_ids[1:]

                if ct_face_value == Decimal(str(0.6)):
                    result = mysql_db.query(sql.format(ct_id, 4))
                    coupon_ids = [row[0] for row in result]
                    new_user_coupon_ids = coupon_ids[:2]
                    invite_user_coupon_ids = coupon_ids[2:]

                if ct_face_value == Decimal(str(0.5)):
                    result = mysql_db.query(sql.format(ct_id, 4))
                    coupon_ids = [row[0] for row in result]
                    new_user_coupon_ids = coupon_ids[:2]
                    invite_user_coupon_ids = coupon_ids[2:]

                if ct_face_value == Decimal(str(0.3)):
                    result = mysql_db.query(sql.format(ct_id, 6))
                    coupon_ids = [row[0] for row in result]
                    new_user_coupon_ids = coupon_ids[:3]
                    invite_user_coupon_ids = coupon_ids[3:]

                if ct_face_value == Decimal(str(0.2)):
                    result = mysql_db.query(sql.format(ct_id, 6))
                    coupon_ids = [row[0] for row in result]
                    new_user_coupon_ids = coupon_ids[:3]
                    invite_user_coupon_ids = coupon_ids[3:]
                if new_user_coupon_ids and invite_user_coupon_ids:
                    ActivitiesTimer.insert_user_coupe(
                        mysql_db, new_user_coupon_ids, new_user, datetime.now(),
                        datetime.now() + timedelta(days=7))
                    ActivitiesTimer.insert_user_coupe(
                        mysql_db, invite_user_coupon_ids,
                        invite_user, datetime.now(),
                        datetime.now() + timedelta(days=7))
            mobile_str = rds_conn.lpop("SHARE_PRESENT_COUPE")


class UserData(object):
    """用户数据"""

    @db.transaction(is_commit=True)
    def user_take_bus_count(self, mysql_cur):
        """
        <用户乘车次数统计>
        """
        order_sql = "SELECT COUNT(`sub_account`),`route_id`,`sub_account` " \
                    "FROM `order` WHERE `pay_time` > '{}' " \
                    "GROUP BY `sub_account`,`route_id`"
        pwc_sql = "SELECT `id` FROM `passenger_weekly_count` " \
                  "WHERE `mobile`='{}' AND `route_id`={}"

        cur_time = datetime.now()
        mysql_db = db.MysqlDbUtil(mysql_cur)
        cur_time = cur_time - timedelta(days=7 + cur_time.weekday())
        # 增加记录
        result = mysql_db.query(order_sql.format(
            cur_time.strftime("%Y-%m-%d 00:00:00")))
        for row in result:
            count = row[0]
            route_id = row[1]
            sub_account = row[2]
            print pwc_sql.format(sub_account, route_id)
            pwc = mysql_db.get(pwc_sql.format(sub_account, route_id))
            if pwc:
                data = {
                    "`id`": pwc[0],
                    "`mobile`": sub_account,
                    "`route_id`": route_id,
                    "`count`": count
                }
                mysql_db.update(data, table_name="`passenger_weekly_count`")
            else:
                data = {
                    "`mobile`": sub_account,
                    "`route_id`": route_id,
                    "`count`": count,
                    "`company_id`": 1  # 无感行
                }
                mysql_db.insert(data, table_name="`passenger_weekly_count`")


class IdentitiesData(object):
    """身份数据"""

    @db.transaction(is_commit=True)
    def change_user_identity_status(self, mysql_cur):
        """
        <修改身份认证状态>
        1.每个用户的身份期限过期,修改状态为已过期(2)
        """
        mysql_db = db.MysqlDbUtil(mysql_cur)
        sql = "SELECT `id`,`end_time` " \
              "FROM `passenger_identity` WHERE `status`=1"
        result = mysql_db.query(sql)
        cur_time = datetime.now()
        for row in result:
            # 当前时间大于截止时间,修改状态
            if cur_time > row[1]:
                d = {"`id`": row[0], "`status`": 2}
                mysql_db.update(d, table_name="`passenger_identity`")


class StatisticsData(object):
    """统计"""

    company_list_sql = "SELECT `id` FROM `company`"

    income_sql = "SELECT SUM(`amount`) FROM `order` WHERE `pay_time` " \
                 "BETWEEN STR_TO_DATE('{}','%Y-%m-%d %H:%i:%s') AND " \
                 "STR_TO_DATE('{}','%Y-%m-%d %H:%i:%s')  AND `company_id`={}"
    passenger_flow_sql = "SELECT COUNT(`id`) FROM `order` " \
                         "WHERE `pay_time` BETWEEN STR_TO_DATE('{}'," \
                         "'%Y-%m-%d %H:%i:%s') AND STR_TO_DATE('{}'," \
                         "'%Y-%m-%d %H:%i:%s') AND `company_id`={}"
    dcccrs_sql = "SELECT COUNT(`tmp`) FROM (SELECT COUNT(`id`) AS tmp FROM " \
                 "`order` WHERE `pay_time` BETWEEN STR_TO_DATE('{}'," \
                 "'%Y-%m-%d %H:%i:%s') AND STR_TO_DATE('{}'," \
                 "'%Y-%m-%d %H:%i:%s') AND `company_id`={} GROUP BY " \
                 "`user_id` HAVING COUNT(`id`)>1) AS tmp_table"
    rate_sql = "SELECT COUNT(`id`) FROM `order` WHERE `pay_time` BETWEEN " \
               "STR_TO_DATE('{}','%Y-%m-%d %H:%i:%s') AND STR_TO_DATE('{}'," \
               "'%Y-%m-%d %H:%i:%s') AND `company_id`={} AND `verify_type`={}"

    @db.transaction(is_commit=True)
    def statistics_yesterday_data(self, mysql_cur):
        """统计昨日数据 10s 执行一次"""
        today = datetime.now()

        if not (today.hour == 0 and today.minute == 1):  # 0 点 1分
            return
        print("time = {} {}".format(today.hour, today.minute))
        mysql_db = db.MysqlDbUtil(mysql_cur)
        yesterday = today - timedelta(days=1)

        zero = Decimal(str(0.0))
        yesterday_begin_str = yesterday.strftime('%Y-%m-%d') + " 00:00:00"
        yesterday_end_str = yesterday.strftime('%Y-%m-%d') + " 23:59:59"

        # 所有公司
        companies = mysql_db.query(StatisticsData.company_list_sql)
        for company in companies:
            company_id = company[0]

            bc_data_sql = \
                "SELECT `id` FROM `bc_every_day_data` WHERE `data_date`='{}' " \
                "AND `company_id`={}".format(
                    yesterday.strftime("%Y-%m-%d"), company_id)
            r = mysql_db.query(bc_data_sql)
            if r:
                continue

            # 昨日收入
            income = mysql_db.get(StatisticsData.income_sql.format(
                yesterday_begin_str, yesterday_end_str, company_id))
            income = income[0] if income[0] else zero

            # 昨日客流
            passenger_flow = mysql_db.get(
                StatisticsData.passenger_flow_sql.format(
                    yesterday_begin_str, yesterday_end_str, company_id))
            passenger_flow = passenger_flow[0] if passenger_flow else 0

            # 多次乘车人数
            dcccrs = mysql_db.get(StatisticsData.dcccrs_sql.format(
                yesterday_begin_str, yesterday_end_str, company_id))
            dcccrs = dcccrs[0] if dcccrs else 0

            # 刷脸支付数量
            face_rate = mysql_db.get(StatisticsData.rate_sql.format(
                yesterday_begin_str, yesterday_end_str, company_id, 2))
            face_rate = face_rate[0] if face_rate else zero

            # IC卡
            ic_card_rate = mysql_db.get(StatisticsData.rate_sql.format(
                yesterday_begin_str, yesterday_end_str, company_id, 3))
            ic_card_rate = ic_card_rate[0] if ic_card_rate else zero

            # 二维码
            qrcode_rate = mysql_db.get(StatisticsData.rate_sql.format(
                yesterday_begin_str, yesterday_end_str, company_id, 1))
            qrcode_rate = qrcode_rate[0] if qrcode_rate else zero

            # 现金
            cash_rate = mysql_db.get(StatisticsData.rate_sql.format(
                yesterday_begin_str, yesterday_end_str, company_id, 4))
            cash_rate = cash_rate[0] if cash_rate else zero

            data = {
                "`kilometre`": 0,
                "`income`": income,
                "`passenger_flow`": passenger_flow,
                "`number_passengers`": passenger_flow,
                "`dcccrs`": dcccrs,
                "face_count": face_rate,
                "ic_card_count": ic_card_rate,
                "qrcode_count": qrcode_rate,
                "cash_count": cash_rate,
                "`face_rate`": face_rate / passenger_flow if passenger_flow else zero,
                "`ic_card_rate`": ic_card_rate / passenger_flow if passenger_flow else zero,
                "`qrcode_rate`": qrcode_rate / passenger_flow if passenger_flow else zero,
                "`cash_rate`": cash_rate / passenger_flow if passenger_flow else zero,
                "`company_id`": company_id,
                "`data_date`": (
                            date.today() - timedelta(days=1)).strftime(
                    '%Y-%m-%d'),
                "`settlement_time`": 'now()'
            }
            mysql_db.insert(data, table_name="`bc_every_day_data`")

    @db.transaction(is_commit=True)
    def statistics_passenger_flow(self, mysql_cur):
        """统计客流 1h"""
        zero = Decimal(str(0.0))
        mysql_db = db.MysqlDbUtil(mysql_cur)

        # 站点客流
        sql = "SELECT COUNT(`id`) FROM `order` WHERE `station_id`={}"
        data_sql = "SELECT `id` FROM `station_passenger_flow` " \
                   "WHERE `station_id`={}"
        stations = mysql_db.query("SELECT `id`,`company_id` FROM `bus_station`")
        for row in stations:
            station_id = row[0]
            company_id = row[1]
            order_numbers = mysql_db.get(sql.format(station_id))
            result = mysql_db.get(data_sql.format(station_id))

            data = {
                "`station_id`": station_id,
                "`number`": order_numbers[0] if order_numbers else zero
            }
            if result:
                data["`id`"] = result[0]
                mysql_db.update(data, table_name="`station_passenger_flow`")
            else:
                data['`company_id`'] = company_id
                mysql_db.insert(data, table_name="`station_passenger_flow`")

        route_pf_sql = "SELECT COUNT(`id`) FROM `order` WHERE `station_id` " \
                       "in (SELECT `bus_station_id` FROM " \
                       "`route_station_relation` WHERE `bus_route_id`={})"
        # 线路客流
        bus_routes = mysql_db.query("SELECT `id`,`company_id` FROM `bus_route`")
        data_sql = "SELECT `id` FROM `route_passenger_flow` WHERE `route_id`={}"

        for row in bus_routes:
            route_id = row[0]
            company_id = row[1]
            result = mysql_db.get(route_pf_sql.format(route_id))
            data = {
                "`route_id`": route_id,
                "`number`": result[0] if result else 0
            }
            result = mysql_db.get(data_sql.format(route_id))
            if result:
                data["`id`"] = result[0]
                mysql_db.update(data, table_name="`route_passenger_flow`")
            else:
                data['`company_id`'] = company_id
                mysql_db.insert(data, table_name="`route_passenger_flow`")
