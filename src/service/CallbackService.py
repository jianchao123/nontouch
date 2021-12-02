# coding:utf-8
import json
from decimal import Decimal
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_

from database.Recharge import Recharge
from database.BusCar import BusCar
from database.BusRoute import BusRoute
from database.FaceImg import FaceImg
from database.Device import Device
from database.UserProfile import UserProfile
from database.Order import Order
from database.UserCoupe import UserCoupe
from database.PassengerIdentity import PassengerIdentity
from database.Coupon import Coupon
from database.db import db
from utils import common
from utils.defines import RedisKey
from ext import cache


class CallbackService(object):

    ALI_SUCCESS_FLAG = ['TRADE_SUCCESS', 'TRADE_FINISHED']

    @staticmethod
    def alipay_callback(out_trade_no, trade_no, trade_status,
                        total_amount, gmt_payment):
        db.session.commit()
        try:
            # 互斥锁
            recharge = db.session.query(Recharge).filter(
                Recharge.order_no == out_trade_no).with_for_update().first()
            print trade_status, CallbackService.ALI_SUCCESS_FLAG
            if trade_status in CallbackService.ALI_SUCCESS_FLAG:
                print recharge.to_whom
                if recharge.to_whom:
                    # 增加余额
                    user = db.session.query(UserProfile).filter(
                        UserProfile.mobile == recharge.to_whom
                    ).with_for_update().first()
                    user.balance += Decimal(str(total_amount))
                    print user.balance
                else:
                    # 增加余额
                    user = db.session.query(UserProfile).filter(
                        UserProfile.id == recharge.user_id
                    ).with_for_update().first()
                    user.balance += Decimal(str(total_amount))
                    print user.balance
                recharge.trade_no = trade_no
                recharge.status = 2  # 成功
                recharge.pay_time = gmt_payment
            elif trade_status == 'TRADE_CLOSED':
                recharge.status = 3  # 失败
                recharge.remark = str(trade_status)

            db.session.commit()
        except SQLAlchemyError:
            import traceback
            print traceback.format_exc()
            db.session.rollback()
            return 'failure'
        finally:
            db.session.close()
        return 'success'

    @staticmethod
    def weixinpay_callback(data):
        import json
        from utils import weixinpay
        from database.UserProfile import UserProfile
        db.session.commit()
        resp_dict = {'return_code': 'FAIL', 'return_msg': 'OK'}
        pay = weixinpay.get_wein_pay(1)  # 默认为APP
        data = pay.to_dict(data)

        if "attach" in data:
            attach = json.loads(data["attach"])
            # 小程序
            if attach["platform_type"] == 2:
                pay = weixinpay.get_wein_pay(2)

        if pay.check(data):
            resp_dict['return_code'] = 'SUCCESS'
            print('验签成功')
            order_no = int(data.get('out_trade_no'))
            recharge = db.session.query(Recharge).filter(
                Recharge.order_no == order_no).with_for_update().first()
            # 记录为待支付中
            if recharge and recharge.status == 1:
                print "======================={} {}".format(recharge.status, data['return_code'])
                recharge.order_no = order_no
                if data['return_code'] == 'SUCCESS':

                    recharge.pay_time = datetime.strptime(
                        data['time_end'], '%Y%m%d%H%M%S')
                    recharge.trade_no = data['transaction_id']

                    if recharge.to_whom:
                        user = db.session.query(UserProfile).filter(
                            UserProfile.mobile == recharge.to_whom
                        ).with_for_update().first()
                        user.balance += recharge.amount
                    else:
                        user = db.session.query(UserProfile).filter(
                            UserProfile.id == recharge.user_id
                        ).with_for_update().first()
                        user.balance += recharge.amount
                    recharge.status = 2  # 成功

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
        finally:
            db.session.close()

        return weixinpay.dict_to_xml(resp_dict)

    @staticmethod
    def create_order(user, data, verify_type, sub_account=None):
        """创建订单
        verify_type
        (1, '无感行二维码'), (2, '人脸'), (3, 'IC卡'), (4, '现金'),
        (5, '微信'), (6, '支付宝'), (7, '银联')
        """
        order = Order()
        order.discount_way = 0
        order.order_no = common.build_pay_order_no(user.id)
        order.route_id = data['route_id']
        order.bus_id = data['bus_id']
        if 'station' in data:
            order.station = data['station']
        order.scan_time = data['scan_time']
        take_bus_amount = Decimal(str(data['amount']))
        # 身份
        from database.Identity import Identity
        identity_objs = db.session.query(PassengerIdentity, Identity).join(
            Identity, Identity.id == PassengerIdentity.identity_id
        ).filter(
            PassengerIdentity.company_id == data["company_id"],
            PassengerIdentity.user_id == user.id,
            PassengerIdentity.status == 1).first()

        coupon = None
        user_coupon = None
        if identity_objs and identity_objs[0] \
                and identity_objs[1] and not sub_account:
            passenger_identity = identity_objs[0]
            identity = identity_objs[1]
            # 免费次数
            if passenger_identity.residue_number:
                order.real_amount = 0
                order.amount = take_bus_amount
                order.discount = take_bus_amount
                order.discount_way = 3  # 免费
                # 更新次数
                passenger_identity.residue_number -= 1
            else:
                # 身份折扣
                real_amount = take_bus_amount * \
                              passenger_identity.discount_rate
                order.real_amount = real_amount
                order.amount = take_bus_amount
                order.discount = take_bus_amount - real_amount
                order.discount_way = 1  # 身份折扣
            d = {"cert": identity.name,
                 "discount_rate": str(passenger_identity.discount_rate)}
            order.content = json.dumps(d)

        else:

            # 该用户是否有优惠券
            objs = db.session.query(Coupon, UserCoupe).join(
                UserCoupe, UserCoupe.coupon_id == Coupon.id).filter(
                and_(UserCoupe.user_id == user.id,
                     Coupon.face_value <= take_bus_amount,
                     Coupon.status == 2,
                     Coupon.use_begin_time < datetime.now(),
                     Coupon.use_end_time > datetime.now())).order_by(
                Coupon.face_value.desc(),
                Coupon.use_end_time.desc()).first()

            if objs and objs[0] and objs[1]:
                coupon = objs[0]
                user_coupon = objs[1]

                face_value = coupon.face_value
                order.real_amount = take_bus_amount - face_value
                order.amount = take_bus_amount
                order.discount = face_value
                order.discount_way = 2

            else:
                order.real_amount = take_bus_amount
                order.amount = take_bus_amount
                order.discount = 0

        if Decimal(str(user.balance)) - order.real_amount < 0:
            return -1
        if coupon and user_coupon:
            # 更新coupon状态
            coupon.status = 3
            user_coupon.use_time = datetime.now()

        order.device_no = data['device_no']
        order.up_stamp = data['up_stamp']
        order.company_id = data["company_id"]
        order.user_id = user.id
        order.pay_time = datetime.now()
        order.state_id = 2  # 支付成功的pk为2
        order.pay_type = 4  # 余额支付
        order.verify_type = verify_type if verify_type else 2  # 为空则是人脸
        if sub_account:
            order.sub_account = sub_account
        else:
            order.sub_account = user.mobile

        # 扣款
        if order.real_amount:
            user.balance -= Decimal(str(order.real_amount))
        order.status = 2
        order.create_time = datetime.now()
        try:
            db.session.add(order)
            db.session.commit()
            return 1
        except SQLAlchemyError:
            import traceback
            print traceback.format_exc()
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def face_callback(device_no, scan_time, mobile, fid):
        db.session.commit()
        is_sub_account = False
        # 判断是否子账户
        if mobile:
            if len(mobile) > 11:
                is_sub_account = True
        else:
            face = db.session.query(FaceImg).filter(
                FaceImg.id == int(fid)).first()
            if len(face.baidu_user_id) > 11:
                is_sub_account = True
                mobile = face.baidu_user_id

        # 从缓存获取设备相关信息
        device_dict = cache.hgetall(device_no)
        if device_dict:
            print device_dict
            bus_id = device_dict[b"bus_id"].decode('utf-8')
            fees = device_dict[b"fees"].decode('utf-8')
            company_id = int(device_dict[b"company_id"].decode('utf-8'))
            route_id = int(device_dict[b"route_id"].decode('utf-8'))
        else:
            device = db.session.query(Device).filter(
                Device.device_no == device_no).with_for_update().first()
            if not device:
                return -10
            car = db.session.query(BusCar).filter(
                BusCar.id == device.car_id).first()
            route = db.session.query(BusRoute).filter(
                BusRoute.id == car.route_id).first()
            device_dict = {
                "bus_id": car.bus_id,
                "fees": float(route.fees),
                "company_id": car.company_id,
                "route_id": route.id
            }
            cache.hmset(device_no, device_dict)
            cache.expire(device_no, 20 * 60)

            bus_id = device_dict["bus_id"]
            fees = device_dict["fees"]
            company_id = device_dict["company_id"]
            route_id = device_dict["route_id"]

        order_params = {"route_id": route_id,
                        "bus_id": bus_id,
                        "amount": fees,
                        "amount_type": 1,
                        "action": 1,
                        "device_no": device_no,
                        "up_stamp": scan_time,
                        "scan_time": scan_time,
                        "company_id": company_id}

        # 设备号+用户号码,控制重复刷脸
        k = "{}:{}".format(device_no, mobile)
        rds_v = cache.get(k)
        print str(rds_v)
        if rds_v:
            return -11
        cache.set(k, 1)
        cache.expire(k, 1 * 60)

        face_img_obj = db.session.query(FaceImg).filter(
            FaceImg.baidu_user_id == mobile).first()
        userprofile = UserProfile.query.filter(
            UserProfile.id == face_img_obj.user_id).first()
        if not userprofile.is_open_face_rgz:
            return -13          # 未开启刷脸功能

        user_mobile = userprofile.mobile
        user_amounts = userprofile.balance

        # 创建订单,扣款
        order_ret = CallbackService.create_order(
            userprofile, order_params, 2,
            mobile if is_sub_account else None)
        if order_ret == -1:     # 余额不足
            return -14
        elif order_ret == -2:   # 提交失败
            return -15

        ret_data = {"mobile": user_mobile,
                    "amounts": str(user_amounts)}

        return ret_data

    @staticmethod
    def qrcode_callback(mobile, device_no, up_time,
                        verify_type, longitude, latitude):
        db.session.commit()
        # 缓存设备相关信息
        rds_conn = cache
        device_dict = rds_conn.hgetall(device_no)
        if device_dict:
            print(str(device_dict))
            bus_id = device_dict[b"bus_id"].decode('utf-8')
            fees = device_dict[b"fees"].decode('utf-8')
            company_id = int(device_dict[b"company_id"].decode('utf-8'))
            route_id = int(device_dict[b"route_id"].decode('utf-8'))
        else:

            device = Device.query.filter(
                Device.device_no == device_no).first()
            if not device_no:
                return -10
            car = db.session.query(BusCar).filter(
                BusCar.id == device.car_id).first()
            route = db.session.query(BusRoute).filter(
                BusRoute.id == car.route_id).first()
            device_dict = {
                "bus_id": car.bus_id,
                "fees": float(route.fees),
                "company_id": car.company_id,
                "route_id": route.id
            }
            rds_conn.hmset(device_no, device_dict)
            rds_conn.expire(device_no, 20 * 60)

            bus_id = device_dict["bus_id"]
            fees = device_dict["fees"]
            company_id = device_dict["company_id"]
            route_id = device_dict["route_id"]

        order_params = {"route_id": route_id,
                        "bus_id": bus_id,
                        "amount": fees,
                        "amount_type": 1,
                        "action": 1,
                        "device_no": device_no,
                        "up_stamp": up_time,
                        "scan_time": up_time,
                        "company_id": company_id}
        # try:
        #     d = get_station_by(device_no, longitude, latitude)
        # except:
        #     logger.error(traceback.format_exc())
        #     d = None
        # if d:
        #     order_params["station"] = \
        #         BusStation.objects.get(id=d["station_id"])  # 站点

        # 获取用户
        userprofile = UserProfile.query.filter(
            UserProfile.mobile == mobile).first()

        # 创建订单,扣款
        order_ret = CallbackService.create_order(
            userprofile, order_params, verify_type)
        if order_ret == -1:
            return -11  # 余额不足
        elif order_ret == -2:
            return -15  # 提交失败
        userprofile = UserProfile.query.filter(
            UserProfile.mobile == mobile).first()
        ret_data = {"mobile": userprofile.mobile,
                    "amounts": str(userprofile.balance)}
        return ret_data

    @staticmethod
    def gps_callback(device_no, lng, lat, timestamp):
        rds_conn = cache
        rds_conn.hset(
            RedisKey.DEVICE_GPS_HASH, device_no, str(lng) + "," + str(lat))
        rds_conn.hset(
            RedisKey.DEVICE_TIMESTAMP_HASH, device_no, str(int(timestamp)))

    @staticmethod
    def temperature_callback(mobile, temperature, scan_timestamp, device_no, gps):
        """
        mobile  可能为空
        """
        db.session.commit()
        from database.Temperature import Temperature
        device = db.session.query(Device).filter(
            Device.device_no == device_no).first()
        car = db.session.query(BusCar).filter(
            BusCar.id == device.car_id).first()
        if not car:
            return -10  # 没有绑定车辆
        t = Temperature()
        t.company_id = device.company_id
        t.mobile = mobile
        t.temperature = float(temperature)
        t.car_no = car.bus_id
        t.device_id = device.id
        t.gps = gps
        t.up_timestamp = round(Decimal(str(scan_timestamp)), 6)
        try:
            db.session.add(t)
            db.session.commit()
            return t.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
