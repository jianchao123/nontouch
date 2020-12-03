# coding:utf-8
from decimal import Decimal
from datetime import timedelta
from sqlalchemy import func
from sqlalchemy import and_, or_
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError

from database.UserProfile import UserProfile
from database.Order import Order
from database.Recharge import Recharge
from database.db import db


class IndexHomeService(object):
    """
       首页数据展示
       {
           "signup_user": {    # 注册用户
               "today": 0,
               "total": 2315,
               "yesterday_rate": 0.0008639308855291577
           },
           "order_total_amount": { # 订单总额
               "yesterday": 0.07993644455068266,
               "today": 2976.0,
               "total": 142238.0
           },
           "signup_user_histogram": [ # 用户柱状图
               ["2019-08-19", 1],
               ["2019-08-20", 0],
               ["2019-08-21", 1],
               ["2019-08-22", 0],
               ["2019-08-23", 2],
               ["2019-08-24", 0],
               ["2019-08-25", 2]
           ],
           "recharge_total_amount": { # 充值总额
               "yesterday": 0.07993644455068266,
               "today": 0.0,
               "total": 142238.0
           },
           "take_bus_histogram": [ # 扫码支付柱状图
               ["2019-08-19", 0],
               ["2019-08-20", 2758],
               ["2019-08-21", 2235],
               ["2019-08-22", 5536],
               ["2019-08-23", 5682],
               ["2019-08-24", 5684],
               ["2019-08-25", 5685]
           ],
           "route_rank_histogram": [ # 线路排行柱状图
               ["2019-08-19", 0],
               ["2019-08-20", 0],
               ["2019-08-21", 0],
               ["2019-08-22", 0],
               ["2019-08-23", 0],
               ["2019-08-24", 0],
               ["2019-08-25", 0]
           ],
           "order_total_amount_histogram": [ # 订单总额柱状图
               ["2019-08-19", 0],
               ["2019-08-20", 5510.0],
               ["2019-08-21", 4456.0],
               ["2019-08-22", 11072.0],
               ["2019-08-23", 11362.0],
               ["2019-08-24", 11368.0],
               ["2019-08-25", 11370.0]
           ],
           "bus_take_number": { # 乘车人次
               "today": 1488,
               "total": 71141,
               "yesterday_rate": 0.0799117246032527
           }
       }

       """

    @staticmethod
    def signup_user_data(today_begin, today_end,
                         yesterday_begin, yesterday_end, company=None):
        """注册用户数据"""
        today_signup_user_count = UserProfile.query.filter(and_(
            UserProfile.date_joined > today_begin,
            UserProfile.date_joined < today_end)).count()

        yesterday_signup_user_count = UserProfile.query.filter(
            and_(UserProfile.date_joined > yesterday_begin,
                 UserProfile.date_joined < yesterday_end)).count()

        total = UserProfile.query.count()

        if company:
            signup_user = {}
        else:
            signup_user = {
                "today": str(today_signup_user_count),
                "yesterday_rate": str(round(
                    yesterday_signup_user_count / float(total),
                    2)) if total else 0,
                "total": str(total)
            }
        return signup_user

    @staticmethod
    def bus_take_number(today_begin, today_end,
                        yesterday_begin, yesterday_end, company=None):
        """乘车人次"""

        today_take_number = Order.query.filter(
            and_(Order.create_time > today_begin,
                 Order.create_time < today_end))

        yesterday_take_number = Order.query.filter(
            and_(Order.create_time > yesterday_begin,
                 Order.create_time < yesterday_end))
        if company:
            today_take_number = today_take_number.filter(
                Order.company_id == company)
            yesterday_take_number = yesterday_take_number.filter(
                Order.company_id == company)
        today_take_number = today_take_number.count()
        yesterday_take_number = yesterday_take_number.count()

        total = Order.query.count()
        bus_take_number = {
            "today": str(today_take_number),
            "yesterday_rate": str(round(yesterday_take_number / float(total),
                                    2)) if total else 0,
            "total": str(total)
        }
        return bus_take_number

    @staticmethod
    def order_total_amount(today_begin, today_end,
                           yesterday_begin, yesterday_end, company=None):
        """订单总额"""
        zero = Decimal(str(0.0))
        today_order_total_amount = Order.query.filter(
            and_(Order.create_time > today_begin,
                 Order.create_time < today_end))

        yesterday_order_total_amount = Order.query.filter(
            and_(Order.create_time > yesterday_begin,
                 Order.create_time < yesterday_end))

        total = db.session.query(Order)

        if company:
            print "--------------------"
            today_order_total_amount = today_order_total_amount.filter(
                Order.company_id == company)
            yesterday_order_total_amount = yesterday_order_total_amount.filter(
                Order.company_id == company)
            total = total.filter(Order.company_id == company)

        today_order_total_amount = today_order_total_amount.with_entities(
            func.Sum(Order.amount)).scalar()
        yesterday_order_total_amount = \
            yesterday_order_total_amount.with_entities(
                func.Sum(Order.amount)).scalar()
        total = total.with_entities(func.Sum(Order.amount)).scalar()
        print today_order_total_amount, yesterday_order_total_amount, total
        today_order_total_amount = \
            today_order_total_amount if today_order_total_amount else zero
        yesterday_order_total_amount = \
            yesterday_order_total_amount if yesterday_order_total_amount else zero
        total = total if total else 0

        order_total_amount = {
            "today": str(today_order_total_amount),
            "yesterday": str(round(yesterday_order_total_amount / total, 2)) if total else 0,
            "total": str(total)
        }
        return order_total_amount

    @staticmethod
    def recharge_total_amount(today_begin, today_end,
                              yesterday_begin, yesterday_end, company_id):
        """充值总额"""
        zero = Decimal(str(0.0))
        today_recharge_total_amount = Recharge.query.filter(
            and_(Recharge.pay_time > today_begin,
                 Recharge.pay_time < today_end)).filter(
            Recharge.company_id == company_id)

        yesterday_recharge_total_amount = Recharge.query.filter(
            and_(Recharge.pay_time > yesterday_begin,
                 Recharge.pay_time < yesterday_end)).filter(
            Recharge.company_id == company_id)

        total = Recharge.query.filter(Recharge.status == 2).filter(
            Recharge.company_id == company_id)  # 成功

        today_recharge_total_amount = \
            today_recharge_total_amount.with_entities(
                func.Sum(Recharge.amount)).scalar()
        yesterday_recharge_total_amount = \
            yesterday_recharge_total_amount.with_entities(
                func.Sum(Recharge.amount)).scalar()
        total = total.with_entities(func.Sum(Recharge.amount)).scalar()

        today_recharge_total_amount = today_recharge_total_amount if today_recharge_total_amount else zero
        yesterday_recharge_total_amount = yesterday_recharge_total_amount if yesterday_recharge_total_amount else zero
        total = total if total else 0

        recharge_total_amount = {
            "today": str(today_recharge_total_amount),
            "yesterday": str(round(yesterday_recharge_total_amount / total,
                               2)) if total else 0,
            "total": str(total)
        }
        return recharge_total_amount

    @staticmethod
    def signup_user_histogram(today, company_id=None):
        """近七日注册用户数"""
        signup_user_histogram = []
        if company_id:
            return signup_user_histogram
        for x in range(7):
            cur_date = today - timedelta(days=7 - x)
            signup_user_histogram.append([cur_date.strftime("%Y-%m-%d"), 0])

        sql = "SELECT LEFT(DATE_FORMAT(`date_joined`,'%Y-%m-%d %H:%i:%s'), " \
              "10) as t, COUNT(`id`) FROM `user_profile` GROUP BY " \
              "LEFT(DATE_FORMAT(`date_joined`,'%Y-%m-%d %H:%i:%s'), 10)" \
              " ORDER BY t DESC LIMIT 7"

        data = {}
        cursor = db.session.execute(sql)
        result = cursor.fetchall()
        for row in result:
            k = row[0].split(" ")[0]
            data[k] = row[1]
        print(data)
        for row in signup_user_histogram:
            if row[0] in data:
                row[1] = str(data[row[0]])

        return signup_user_histogram

    @staticmethod
    def take_bus_histogram(today, company_id=None):
        """近七日乘车人数"""
        sql = "SELECT LEFT(DATE_FORMAT(`create_time`,'%Y-%m-%d %H:%i:%s'), " \
              "10) as t, COUNT(`id`) FROM `order` {} GROUP BY " \
              "LEFT(DATE_FORMAT(`create_time`,'%Y-%m-%d %H:%i:%s'), 10) " \
              "ORDER BY t DESC LIMIT 7"
        if company_id:
            sql = sql.format(" WHERE `company_id`={} ".format(company_id))
        else:
            sql = sql.format(" ")

        take_bus_histogram = []
        for x in range(7):
            cur_date = today - timedelta(days=7 - x)
            take_bus_histogram.append([cur_date.strftime("%Y-%m-%d"), 0])
        data = {}
        cursor = db.session.execute(sql)
        result = cursor.fetchall()
        for row in result:
            k = row[0].split(" ")[0]
            data[k] = row[1]
        for row in take_bus_histogram:
            if row[0] in data:
                row[1] = str(data[row[0]])

        return take_bus_histogram

    @staticmethod
    def order_total_amount_histogram(today, company_id=None):
        """近七日订单总额"""
        sql = "SELECT LEFT(DATE_FORMAT(`create_time`,'%Y-%m-%d %H:%i:%s'), " \
              "10) as t, SUM(`amount`) FROM `order` {}" \
              "GROUP BY LEFT(DATE_FORMAT(`create_time`,'%Y-%m-%d %H:%i:%s'), " \
              "10) ORDER BY t DESC LIMIT 7"
        if company_id:
            sql = sql.format(" WHERE `company_id`={} ".format(company_id))
        else:
            sql = sql.format(" ")
        print sql
        order_total_amount_histogram = []
        for x in range(7):
            cur_date = today - timedelta(days=7 - x)
            order_total_amount_histogram.append(
                [cur_date.strftime("%Y-%m-%d"), 0])
        data = {}
        cursor = db.session.execute(sql)
        result = cursor.fetchall()
        for row in result:
            k = row[0].split(" ")[0]
            data[k] = row[1]
        for row in order_total_amount_histogram:
            if row[0] in data:
                row[1] = str(data[row[0]])

        return order_total_amount_histogram

    @staticmethod
    def route_rank_histogram(today, company_id=None):
        """线路流量排行"""

        sql = "SELECT br.`line_no`, COUNT(o.`id`) FROM `bus_route` as br " \
              "INNER JOIN `order` as o ON o.`route_id`=br.id {} " \
              "GROUP BY br.`id`"
        if company_id:
            sql = sql.format(" WHERE br.`company_id`={} ".format(company_id))
        else:
            sql = sql.format(" ")

        data = []
        cursor = db.session.execute(sql)
        result = cursor.fetchall()
        for row in result:
            data.append([row[0] + "路", row[1]])
        return data

