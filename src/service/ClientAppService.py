# coding:utf-8
import base64
import requests
from datetime import datetime
from decimal import Decimal
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

from database.db import db
from database.UserProfile import UserProfile
from database.Recharge import Recharge
from database.Configure import Configure
from database.UserCoupe import UserCoupe
from database.Coupon import Coupon
from database.CouponType import CouponType
from database.FaceImg import FaceImg
from database.DistrictCode import DistrictCode
from database.Application import Application
from database.LostAndFound import LostAndFound
from database.Identity import Identity
from database.Company import Company
from database.Certification import Certification
from database.Bill import Bill
from database.BillDetail import BillDetail
from database.Order import Order
from database.PassengerIdentity import PassengerIdentity

from ext import cache
from utils import smscode
from utils.validators import mobile_validate
from utils.tools import md5_encrypt, gen_token
from utils import scan
from utils import face
from ext import conf
from utils import pay
from utils import weixinpay


class ClientAppService(object):
    MOBILE_CACHE_KEY = 'smscode:mobile:{}:{}'
    TOKEN_ID_KEY = 'hash:token.id:{}'
    INVALID_USER_ID = -1
    USER_OPERATIONS = 'mysql_user:operations:{}'

    @staticmethod
    def get_user_by_mobile(mobile):
        db.session.commit()

        user = db.session.query(UserProfile).filter(
            UserProfile.mobile == mobile).first()
        if not user:
            return None
        return {'id': user.id, 'mobile': user.mobile, 'password': user.password}

    @staticmethod
    def send_verify_code(mobile, code_type):
        """
        发送验证码
        :param mobile
        :param code_type    1注册 2修改密码 3登陆
        """
        db.session.commit()

        if code_type not in (1, 2, 3):
            return -4  # 参数错误

        if not mobile_validate(mobile):
            return -10  # APP_USER_PHONE_NUMBER_ILLEGALITY
        user_profile = db.session.query(UserProfile).filter(
            UserProfile.mobile == mobile).first()
        if user_profile and code_type == 1:
            return -11  # APP_USER_PHONE_NUMBER_REGISTERED
        if not user_profile and code_type in (2, 3):
            return -12  # APP_USER_PHONE_NUMBER_UNREGISTER
        k = ClientAppService.MOBILE_CACHE_KEY.format(code_type, mobile)
        if cache.get(k):
            return -13  # APP_USER_ONE_MINUTE_SEND

        rand_code = smscode.randomCode()
        res = smscode.send_code_ali(mobile, rand_code, type=code_type)
        if not res:
            print(u'%s 验证码 %s 发送失败', mobile, rand_code)
            return -14  # APP_USER_VERIFICATION_CODE_SENDING_FAIL
        cache.set(k, rand_code)
        cache.expire(k, 60)
        return {}

    @staticmethod
    def login(user_id, token):
        cache.set(ClientAppService.TOKEN_ID_KEY.format(token), user_id)
        cache.expire(ClientAppService.TOKEN_ID_KEY.format(token), 60 * 60 * 2)

    @staticmethod
    def signin(mobile, password):
        """登录"""
        db.session.commit()

        user_obj = ClientAppService.get_user_by_mobile(mobile)
        if not user_obj:
            return -1
        print user_obj
        password_md5_str = md5_encrypt(password)
        if user_obj["password"] != password_md5_str:
            return -10
        token = gen_token(password, conf.config["SALT"], 3600)
        ClientAppService.login(user_obj['id'], token)
        return {
            'token': token,
            'mysql_user': {
                'id': user_obj['id'],
                'mobile': user_obj['mobile']
            }
        }

    @staticmethod
    def signup(mobile, password, code, invite_code=None):
        """注册"""
        db.session.commit()
        user = db.session.query(UserProfile).filter(
            UserProfile.mobile == mobile).first()
        if user:
            return -10  # 用户已经存在
        ks = cache.get(ClientAppService.MOBILE_CACHE_KEY.format(1, mobile))
        if ks and str(ks) != str(code):
            return -11  # 验证码错误

        try:
            user = UserProfile()
            user.mobile = mobile
            user.password = md5_encrypt(password)
            user.username = mobile
            user.is_active = 1
            user.balance = 0.0
            user.is_open_face_rgz = 0
            user.company_id = 1  # 默认为无感行
            user.email = mobile + '@wgx.com'
            user.nickname = mobile
            user.id_card = ""
            user.avatar = ""
            user.gender = 1
            user.birthday = datetime.now().today()

            db.session.add(user)
            db.session.commit()
            if invite_code:
                cache.rpush("SHARE_PRESENT_COUPE",
                            user.mobile + ":" + str(invite_code))

            return {'id': user.id}
        except SQLAlchemyError:
            import traceback
            print traceback.format_exc()
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def user_info(user_id):
        """
        用户信息
        """
        db.session.commit()
        user_profile = db.session.query(UserProfile).filter(
            UserProfile.id == user_id).first()
        d = defaultdict()
        d['id'] = user_profile.id
        d['mobile'] = user_profile.mobile
        d['nickname'] = user_profile.nickname
        d['balance'] = str(user_profile.balance)
        d['avatar'] = user_profile.avatar
        d['gender'] = user_profile.gender
        d['birthday'] = user_profile.birthday.strftime('%Y-%m-%d')
        d['is_open_face_rgz'] = True if user_profile.is_open_face_rgz else False

        # 是否充值超过5元
        amounts = db.session.query(Recharge).filter(
            Recharge.user_id == user_id).with_entities(
            func.sum(Recharge.amount)).all()
        d['is_recharge'] = 1 if amounts[0] >= Decimal(str(5.0)) else 0

        # 配置
        def get_content():
            o = Configure.query.filter(Configure.key == "open").first()
            if int(o.value):
                configure = Configure.query.filter(
                    Configure.key == "hidden_content").first()
                return configure.value
            else:
                return ""

        d['content'] = get_content()

        # 优惠券
        coupon_number = db.session.query(UserCoupe).join(
            Coupon, Coupon.id == UserCoupe.coupon_id).filter(
            UserCoupe.user_id == user_id, Coupon.status == 2).count()
        d['coupon_number'] = coupon_number
        return d

    @staticmethod
    def change_user(user_id, nickname, avatar, gender, birthday):
        """
        修改用户信息
        更新昵称: { "nickname": ""}
        更新性别: { "gender": (0:保密，1:男，2:女) }
        更新生日: { "birthday": "2019-03-13" }
        更新头像：form-data上传文件 { key: avatar, value: 头像文件}
        更新密码: { "password": "", "code": ""} code 根据获取验证码就扣接口获取，传入type=2
        开启关闭人脸： is_open_face_rgz  True | False
        """
        db.session.commit()
        user = db.session.query(UserProfile).filter(
            UserProfile.id == user_id).first()
        if nickname:
            user.nickname = nickname
        if avatar:
            user.avatar = avatar
        if gender:
            user.gender = gender
        if birthday:
            user.birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
        try:
            db.session.commit()
            return {'id': user.id}
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def forget_pwd(mobile, code, password):
        """
        忘记密码
        """
        db.session.commit()
        user = db.session.query(UserProfile).filter(
            UserProfile.mobile == mobile).first()
        if not user:
            return -10  # 用户不存在
        ks = cache.get(ClientAppService.MOBILE_CACHE_KEY.format(2, mobile))
        if ks and str(ks) != str(code):
            return -11  # 验证码错误

        try:
            user.password = md5_encrypt(password)
            db.session.commit()
            return {'id': user.id}
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def get_qrcode(user_id):
        """
        APP获取乘车二维码
        """
        db.session.commit()
        user = db.session.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        if user.balance == Decimal(str(0.0)):
            raise -10  # APP_USER_BALANCE_INSUFFICIENT
        data = defaultdict()
        data['mysql_user'] = str(user.mobile)
        result = scan.add_sign(data)
        return {'qrcode': result}

    @staticmethod
    def user_coupon_list(user_id, status):
        """
        用户优惠券
        """
        db.session.commit()
        sets = db.session.query(Coupon, CouponType).join(
            UserCoupe, UserCoupe.coupon_id == Coupon.id).join(
            CouponType, CouponType.id == Coupon.type_id).filter(
            UserCoupe.user_id == user_id).filter(Coupon.status == status)
        results = []
        for row in sets:
            coupon = row[0]
            coupon_type = row[1]
            results.append({
                'id': coupon.id,
                'use_begin_time':
                    coupon.use_begin_time.strftime("%Y-%m-%d %H:%M:%S"),
                'use_end_time':
                    coupon.use_end_time.strftime("%Y-%m-%d %H:%M:%S"),
                'img_url': coupon_type.img_url,
                'name': coupon_type.name,
                'face_value': str(coupon.face_value),
                'status': coupon.status,
                'code': coupon.code
            })
        return {'results': results}

    @staticmethod
    def receive_coupon(user_id, code):
        """领取优惠券"""
        db.session.commit()
        coupon = db.session.query(Coupon).filter(
            Coupon.code == code).first()
        if not coupon:
            return -12
        if coupon.status != 1:
            return -10  # 优惠券状态错误

        cur_time = datetime.now()
        coupon_type = db.session.query(CouponType).filter(
            CouponType.id == coupon.type_id).first()
        if not (coupon_type.give_out_begin_time < cur_time <
                coupon_type.give_out_end_time) or coupon_type.status != 2 or \
                not coupon_type.is_online:
            return -11  # COUPON_ACTIVITY_NOT_STARTING

        try:
            # 状态修改为已发放
            coupon.status = 2

            user_coupe = UserCoupe()
            user_coupe.user_id = user_id
            user_coupe.coupon_id = coupon.id
            user_coupe.get_time = datetime.now()
            user_coupe.company_id = 1   # 无感行
            db.session.add(user_coupe)
            db.session.commit()
            return {'id': coupon.id}
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def open_face_recognition(user_id, open_or_close):
        """
        打开或关闭人脸识别 (APP)
        """
        db.session.commit()
        user = db.session.query(UserProfile).filter(
            UserProfile.id == user_id).first()
        try:
            user.is_open_face_rgz = open_or_close
            db.session.commit()
            return {'id': user.id}
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def get_user_face_status(user_id):
        """
        获取人脸开关状态 (APP)
        """
        db.session.commit()
        user = db.session.query(UserProfile).filter(
            UserProfile.id == user_id).first()
        is_open_face_rgz = True if user.is_open_face_rgz else False
        return {'is_open_face_rgz': is_open_face_rgz}

    @staticmethod
    def face_image_list(user_id):
        db.session.commit()
        users = db.session.query(FaceImg).filter(
            FaceImg.user_id == user_id, FaceImg.status == 1)
        data = []
        for row in users:
            data.append({
                "id": row.id,
                "baidu_user_id": row.baidu_user_id,
                "oss_url": row.oss_url,
                "parent_mobile": row.parent_mobile,
                "is_sub_account": True if row.is_sub_account else False,
                "sub_account_name": row.sub_account_name
            })
        return {'results': data}

    @staticmethod
    def face_image_change(user_id, baidu_user_id, oss_url, sub_account_name):
        """
        修改人脸信息
        :param user_id: 必须
        :param baidu_user_id: 必须
        :param oss_url:
        :param sub_account_name:
        :return:
        """
        db.session.commit()
        instance = db.session.query(FaceImg).filter(
            FaceImg.baidu_user_id == baidu_user_id).first()

        try:
            # 向百度更新人脸
            if oss_url:
                group_id = conf.config['BAIDU_GROUP_ID']
                res = requests.get(oss_url)
                image = base64.b64encode(res.content).decode("utf8")
                # 更新人脸
                d = face.rgn_client.updateUser(
                    image, "BASE64", group_id, baidu_user_id)
                # 用户不存在
                if d["error_code"] == 223103:
                    return -10
                face_id = d["result"]["face_token"]
                instance.oss_url = oss_url
                instance.face_id = face_id
                instance.face_last_time = datetime.now()  # 人脸最后更新时间

            if sub_account_name:
                instance.sub_account_name = sub_account_name
            db.session.commit()
            return {
                'id': instance.id,
                'baidu_user_id': instance.baidu_user_id,
                'group_id': instance.group_id,
                'oss_url': instance.oss_url,
                'is_sub_account': instance.is_sub_account,
                'sub_account_name': instance.sub_account_name,
                'face_id': instance.face_id,
                'status': instance.status
            }
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def face_image_delete(pk):
        """
        删除face_image
        """
        db.session.commit()
        face_image = db.session.query(FaceImg).filter(
            FaceImg.id == pk).first()
        if face_image.status != 1:
            return -10
        if not face_image.is_sub_account:
            return -11
        try:
            face_image.status = 10
            face.rgn_client.deleteUser(
                conf.config['BAIDU_GROUP_ID'],
                face_image.baidu_user_id)
            db.session.commit()
            return {'id': face_image.id}
        except:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def face_image_add(user_id, oss_url, is_sub_account, sub_account_name):
        """
        ----oss_url string 必须 该图片在oss的路径
        ----is_sub_account int 必须 是否子账户,取值0|1
        ----sub_account_name string 可选 子账户名字
        """
        flag = 0
        db.session.commit()
        try:
            user = db.session.query(UserProfile).filter(
                UserProfile.id == user_id).first()
            # 当前用户 baidu_user_id的后缀
            if is_sub_account:
                last_face_image = FaceImg.query.filter(
                    FaceImg.user_id == user_id).order_by(
                    FaceImg.id.desc()).first()
                if last_face_image:
                    s = last_face_image.baidu_user_id.split("_")
                    if len(s) == 1:
                        suffix = '01'
                    else:
                        suffix = "%02d" % (int(s[-1]) + 1)
                else:
                    suffix = "01"
                baidu_user_id = user.mobile + "_" + suffix
                parent_mobile = user.mobile
            else:
                baidu_user_id = user.mobile

            # 检测是否已经注册
            is_register = db.session.query(FaceImg).filter(
                FaceImg.baidu_user_id == baidu_user_id).count()
            if is_register:
                return -11

            # 向百度注册人脸
            data = None
            try:
                res = requests.get(oss_url)
                image = base64.b64encode(res.content).decode("utf8")
                data = face.rgn_client.addUser(
                    image, "BASE64", conf.config['BAIDU_GROUP_ID'],
                    baidu_user_id)
            except:
                import traceback
                print traceback.format_exc()
            if data and data["error_code"] == 223105:
                return -10  # CERT_REPETITION_REGISTER_FACE

            face_image = FaceImg()
            face_image.baidu_user_id = baidu_user_id
            face_image.group_id = conf.config['BAIDU_GROUP_ID']
            face_image.oss_url = oss_url
            if is_sub_account:
                face_image.parent_mobile = parent_mobile
                face_image.sub_account_name = sub_account_name
            face_image.is_sub_account = is_sub_account
            face_image.face_id = data["result"]["face_token"]
            face_image.face_last_time = datetime.now()
            face_image.user_id = user_id
            face_image.img = ""
            face_image.status = 1  # 有效
            face_image.company_id = 1 # 无感行
            db.session.add(face_image)
            db.session.commit()
            return {'id': face_image.id,
                    'baidu_user_id': face_image.baidu_user_id,
                    'group_id': face_image.group_id,
                    'oss_url': face_image.oss_url,
                    'parent_mobile': face_image.parent_mobile,
                    'sub_account_name': face_image.sub_account_name,
                    'is_sub_account': face_image.is_sub_account,
                    'face_id': face_image.face_id,
                    'face_last_time':
                        face_image.face_last_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'user_id': face_image.user_id,
                    'status': face_image.status}
        except:
            import traceback
            print traceback.format_exc()
            flag = 1
            db.session.rollback()
            return -2
        finally:
            db.session.close()
            if flag:
                face.rgn_client.deleteUser(
                    conf.config['BAIDU_GROUP_ID'], baidu_user_id)

    @staticmethod
    def user_recharges(user_id, is_open_bill, last_pk):
        """
        用户的充值记录
        is_open_bill 1-已开具的 2-未开具的
        """
        from database.BillDetail import BillDetail
        from database.Bill import Bill
        db.session.commit()
        query = db.session.query(Recharge)
        if is_open_bill:
            is_open_bill = int(is_open_bill)
            bill_detail_sets = db.session.query(BillDetail).join(
                Bill, Bill.id == BillDetail.bill_id).filter(
                Bill.user_id == user_id).all()
            recharge_ids = [row.recharge_id for row in bill_detail_sets]
            if is_open_bill == 1:
                query = query.filter(Recharge.id.in_(recharge_ids))
            elif is_open_bill == 2:
                query = query.filter(Recharge.id.notin_(recharge_ids))
            query = query.filter(
                Recharge.user_id == user_id, Recharge.status == 2)
        else:
            query = query.filter(Recharge.user_id == user_id)

        query = query.order_by(Recharge.id.desc())
        if last_pk:
            query = query.filter(Recharge.id < int(last_pk))
            query = query.limit(10)
        sets = query.all()
        results = []
        for row in sets:
            d = defaultdict()
            d['pk'] = row.id
            d['user_id'] = row.user_id
            d['name'] = row.name
            d['amount'] = str(row.amount)
            d['body'] = row.body
            d['pay_type'] = row.pay_type
            d['to_whom'] = row.to_whom
            d['order_no'] = row.order_no
            d['state'] = row.status
            d['create_time'] = row.create_time.strftime('%Y-%m-%d %H:%M:%S')
            results.append(d)
        return {'results': results}

    @staticmethod
    def get_sign(data):
        data.pop('pay_type')
        res = pay.add_sign(data)
        return res

    @staticmethod
    def user_recharge_add(user_id, name, pay_type, amount,
                          to_whom, remote_addr, is_mini):
        """统一下单
        'mysql_user', 'name', 'amount', 'pay_type', body, to_whom

        """
        print name, pay_type, amount, to_whom, remote_addr, is_mini
        from utils import common
        db.session.commit()
        user = db.session.query(UserProfile).filter(
            UserProfile.id == user_id).first()

        recharge = Recharge()
        recharge.user_id = user_id
        recharge.name = name
        recharge.amount = round(amount, 2)
        recharge.order_no = common.build_recharge_order_no(str(user_id))
        if to_whom:
            recharge.to_whom = to_whom
        recharge.user_id = user_id
        recharge.company_id = 1  # 默认无感行
        recharge.pay_type = pay_type
        recharge.remark = ""
        recharge.status = 1
        try:
            db.session.add(recharge)
            db.session.commit()

            data = {'mysql_user': user_id, 'name': name.encode('utf-8'),
                    'pay_type': pay_type, 'amount': amount, 'body': '',
                    'to_whom': to_whom, 'order_no': recharge.order_no}
            # 支付宝
            if pay_type == 1:
                sign = ClientAppService.get_sign(data)
                return {'results': sign}
            # 微信
            elif pay_type == 2:
                if is_mini:
                    raw = weixinpay.get_unified_ordering(
                        data, remote_addr, platform_type=2,
                        openid=user.wx_open_id)
                else:
                    raw = weixinpay.get_unified_ordering(data, remote_addr)
                return raw
        except SQLAlchemyError:
            import traceback
            print traceback.format_exc()
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def user_recharge_change(order_no, remote_addr):
        """
        用户充值 (支付旧的订单)
        :return:
        """
        db.session.commit()
        instance = db.session.query(Recharge).filter(
            Recharge.order_no == str(order_no)).first()
        if instance.status != 1:
            return -10  # ORDER_UNABLE_RECALL

        data = {'mysql_user': instance.user_id, 'name': instance.name.encode('utf-8'),
                'amount': instance.amount, 'body': instance.body,
                'to_whom': instance.to_whom, 'pay_type': instance.pay_type,
                'order_no': instance.order_no}
        if instance.pay_type == 1:
            return {'results': ClientAppService.get_sign(data)}
        elif instance.pay_type == 2:
            return weixinpay.get_unified_ordering(data, remote_addr)

    @staticmethod
    def user_orders(user_id):
        """
        'id', 'discount', 'real_amount', 'discount_way', 'line_no',
                  'station', 'scan_time', 'bus_id', 'mobile', 'amount',
                  'state', 'verify_type', 'order_no', 'create_time', 'pay_time',
                  'content', 'company_name'
        """
        db.session.commit()
        from database.BusRoute import BusRoute
        from database.BusStation import BusStation
        from database.Company import Company
        from database.Order import Order

        sets = db.session.query(Order, BusRoute, UserProfile, Company).join(
            BusRoute, BusRoute.id == Order.route_id).join(
            UserProfile, UserProfile.id == Order.user_id).join(
            Company, Company.id == Order.company_id).filter(
            Order.user_id == user_id).order_by(Order.id.desc()).all()
        results = []
        for row in sets:
            order = row[0]
            route = row[1]
            user = row[2]
            company = row[3]

            if order.station_id:
                bus_station = db.session.query(BusStation).filter(
                    BusStation.id == order.station_id).first()
                station_name = bus_station.name
            else:
                station_name = ''
            results.append({
                'id': order.id,
                'discount': order.discount,
                'real_amount': order.real_amount,
                'discount_way': order.discount_way,
                'line_no': route.line_no,
                'scan_time': order.scan_time.strftime('%Y-%m-%d %H:%M:%S'),
                'bus_id': order.bus_id,
                'mobile': user.mobile,
                'amount': order.amount,
                'state': order.status,
                'verify_type': order.verify_type,
                'order_no': order.order_no,
                'create_time': order.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'pay_time': order.pay_time.strftime('%Y-%m-%d %H:%M:%S'),
                'content': order.content,
                'station': station_name,
                'company_name': company.name
            })
        return {'results': results}

    @staticmethod
    def district_code_list():
        result = []
        queryset = db.session.query(DistrictCode).all()
        for q in queryset:
            if q.level == 1:
                province = defaultdict()
                province['name'] = q.name
                province['id'] = q.ad
                province["pk"] = q.id
                province['city'] = []
                result.append(province)
            elif q.level == 2:
                city = defaultdict()
                city['name'] = q.name
                city['id'] = q.ad
                city["pk"] = q.id
                city['county'] = []
                province['city'].append(city)
            else:
                county = defaultdict()
                county['name'] = q.name
                county['id'] = q.ad
                county["pk"] = q.id
                if city.get('county') is not None:
                    city['county'].append(county)
        return {'results': result}

    @staticmethod
    def app_version():
        db.session.commit()
        application = db.session.query(Application).order_by(
            Application.version_code.desc()).first()
        return {
            'id': application.id,
            'name': application.name,
            'update_content': application.update_content,
            'version': application.version,
            'version_code': application.version_code,
            'update_force': True if application.update_force else False,
            'url': application.url
        }

    @staticmethod
    def feedback_add(user_id, content):
        """添加用户反馈"""
        db.session.commit()
        from database.Feedback import Feedback
        feedback = Feedback()
        feedback.start_time = datetime.now()
        feedback.type_id = 'APP'
        feedback.user_id = user_id
        feedback.content = content
        feedback.remarks = ""
        feedback.company_id = 1  # 五感行
        try:
            db.session.add(feedback)
            db.session.commit()
            return {'id': feedback.id}
        except SQLAlchemyError:
            import traceback
            print traceback.format_exc()
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def notice_list(start_time_str):
        db.session.commit()
        from database.Notice import Notice
        query = db.session.query(Notice).filter(Notice.is_active == 1)
        if start_time_str:
            start_time_raw = datetime.strptime(start_time_str,
                                               '%Y-%m-%d %H:%M:%S')
            query = query.filter(Notice.start_time > start_time_raw)
        notices = query.order_by(Notice.create_time.desc()).all()
        results = []
        for row in notices:
            d = defaultdict()
            d['id'] = row.id
            d['name'] = row.name
            d['content'] = row.content
            d['content'] = row.content
            d['create_time'] = row.create_time.strftime('%Y-%m-%d %H:%M:%S')
            d['start_time'] = row.start_time.strftime('%Y-%m-%d %H:%M:%S')
            d['end_time'] = row.end_time.strftime('%Y-%m-%d %H:%M:%S')
            d['priority'] = row.priority
            d['is_active'] = row.is_active
            results.append(d)
        return {'results': results}

    @staticmethod
    def advert_list(adv_location):
        db.session.commit()
        from database.Advert import Advert
        from sqlalchemy import and_
        adverts = db.session.query(Advert).filter(
            and_(Advert.is_active == 1,
                 Advert.end_time > datetime.now()))
        if adv_location:
            adverts = adverts.filter(Advert.adv_location == adv_location)

        adverts = adverts.order_by(Advert.create_time.desc()).all()
        results = []
        for row in adverts:
            d = defaultdict()
            d['id'] = row.id
            d['name'] = row.name
            d['image'] = row.image
            d['url'] = row.url
            d['create_time'] = row.create_time.strftime('%Y-%m-%d %H:%M%:S')
            d['start_time'] = row.start_time.strftime('%Y-%m-%d %H:%M%:S')
            d['end_time'] = row.end_time.strftime('%Y-%m-%d %H:%M%:S')
            d['is_active'] = True if row.is_active else False
            d['adv_location'] = row.adv_location
            results.append(d)
        return {'results': results}

    @staticmethod
    def lostandfound_list(user_id, is_query_me):
        db.session.commit()
        query = db.session.query(LostAndFound).filter(LostAndFound.status != 10)
        if is_query_me and int(is_query_me):
            query = query.filter(LostAndFound.create_user_id == user_id)
        lost_and_founds = query.all()
        results = []
        for row in lost_and_founds:
            d = defaultdict()
            d['id'] = row.id
            d['description'] = row.description
            d['city'] = row.city
            d['line_no'] = row.line_no
            d['contacts'] = row.contacts
            d['status'] = row.status
            d['imgs'] = row.imgs
            d['is_admin_publish'] = True if row.is_admin_publish else False
            d['create_user_id'] = row.create_user_id
            d['create_time'] = row.create_time.strftime('%Y-%m-%d %H:%M:%S')
            if user_id == row.create_user_id:
                d['is_me'] = True
            else:
                d['is_me'] = False
            results.append(d)
        return {'results': results}

    @staticmethod
    def lostandfound_add(user_id, description, city, line_no, contacts, imgs):
        db.session.commit()
        lost = LostAndFound()
        lost.description = description
        lost.city = city
        lost.line_no = line_no
        lost.contacts = contacts
        lost.imgs = imgs
        lost.create_user_id = user_id
        lost.is_admin_publish = 0
        lost.company_id = 1 # 五感行
        lost.status = 1
        try:
            db.session.add(lost)
            db.session.commit()
            return {'id': lost.id}
        except SQLAlchemyError:
            db.session.rollback()
            import traceback
            print traceback.format_exc()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def lostandfound_change(pk, status):
        db.session.commit()
        lost = LostAndFound.query.filter(LostAndFound.id == pk).first()
        lost.status = status
        lost.is_admin_publish = 0
        try:
            db.session.commit()
            return {'id': lost.id}
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def lostandfound_retrieve(pk, user_id):
        db.session.commit()
        row = LostAndFound.query.filter(LostAndFound.id == pk).first()
        d = defaultdict()
        d['id'] = row.id
        d['description'] = row.description
        d['city'] = row.city
        d['line_no'] = row.line_no
        d['contacts'] = row.contacts
        d['status'] = row.status
        d['imgs'] = row.imgs
        d['is_admin_publish'] = row.is_admin_publish
        d['create_user_id'] = row.create_user_id
        d['create_time'] = row.create_time.strftime('%Y-%m-%d %H:%M%:S')
        if user_id == row.create_user_id:
            d['is_me'] = True
        else:
            d['is_me'] = False
        return d

    @staticmethod
    def identity_list(company_id):
        db.session.commit()

        identities = db.session.query(Identity, Company).join(
            Company, Company.id == Identity.company_id).filter(
            Identity.company_id == company_id, Identity.status == 1).all()
        results = []
        for row in identities:
            identity = row[0]
            company = row[1]

            d = defaultdict()
            d['id'] = identity.id
            d['name'] = identity.name
            d['company'] = identity.company_id
            d['company_name'] = company.name
            d['create_time'] = identity.create_time.strftime('%Y-%m-%d %H:%M:%S')
            d['description'] = identity.description
            results.append(d)
        return {'results': results}

    @staticmethod
    def certification_list(user_id):
        db.session.commit()
        certification = db.session.query(Certification, Company, Identity,
                                         UserProfile).join(
            Company, Company.id == Certification.company_id).join(
            Identity, Identity.id == Certification.identity_id).join(
            UserProfile, UserProfile.id == Certification.user_id).filter(
            Certification.user_id == user_id, Certification.status != 4).all()
        results = []
        for row in certification:
            cert = row[0]
            company = row[1]
            identity = row[2]
            user = row[3]
            d = defaultdict()
            d['pk'] = cert.id
            d['company_name'] = company.name
            d['company'] = company.id
            d['identity_name'] = identity.name
            d['identity'] = identity.id
            d['user_mobile'] = user.mobile
            d['user_signup_time'] = user.date_joined.strftime(
                '%Y-%m-%d %H:%M:%S')
            d['mysql_user'] = user.id
            d['user_balance'] = str(user.balance)
            d['upload_imgs'] = cert.upload_imgs
            d['status'] = cert.status
            d['date_of_approval'] = cert.date_of_approval.strftime(
                '%Y-%m-%d %H:%M:%S')
            d['pass_reason'] = cert.pass_reason
            if cert.status == 2:
                pi = PassengerIdentity.query.filter(
                    PassengerIdentity.certification_id == cert.id).first()
                d['is_end'] = pi.status == 2
                d['end_time'] = pi.end_time.strftime('%Y-%m-%d %H:%M:%S')
            results.append(d)
        return {'results': results}

    @staticmethod
    def certification_commit(company_id, identity_id, user_id, upload_imgs):
        db.session.commit()
        count = db.session.query(Certification).join(
            PassengerIdentity,
            PassengerIdentity.certification_id == Certification.id).filter(
            Certification.company_id == company_id,
            Certification.user_id == user_id,
            Certification.status.in_([1, 2]),
            Certification.identity_id == identity_id,
            PassengerIdentity.status == 1   # 生效中
        ).count()

        if count:
            return -10
        cert = Certification()
        cert.company_id = company_id
        cert.identity_id = identity_id
        cert.user_id = user_id
        cert.status = 1  # 审核中
        cert.upload_imgs = upload_imgs
        try:
            db.session.add(cert)
            db.session.commit()
            return {'id': cert.id}
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def cert_query_company(user_id):
        db.session.commit()
        user = UserProfile.query.filter(UserProfile.id == user_id).first()
        companies = Company.query.filter(Company.status == 1).all()  # 启用中的公司
        d = []
        for row in companies:
            certifications = Certification.query.filter(
                Certification.company_id == row.id,
                Certification.user_id == user.id).all()
            status = 0
            for certification in certifications:
                if certification.status == 1 and 3 > status:
                    status = 3

                if certification.status == 2 and 4 > status:
                    passenger_identity = PassengerIdentity.query.filter(
                        PassengerIdentity.certification_id == certification.id
                    ).first()
                    if passenger_identity.status == 2:
                        status = 1
                    if passenger_identity.status == 1:
                        status = 4

                if certification.status == 3 and 2 > status:
                    status = 2
            d.append({
                "name": row.name,
                "id": row.id,
                "company_id": row.id,
                "status": status
            })
        return {'results': d}

    @staticmethod
    def create_bill(user_id, headline, headline_type, bank_name, bank_account,
                    email, enterprise_name, bill_no, enterprise_address,
                    enterprise_phone, recharge_pks):
        """
            ----headline 抬头
            ----headline_type 抬头类型 1-企业 2-个人
            ----bank_name
            ----bank_account
            ----email
            ----enterprise_name
            ----bill_no
            ----enterprise_address
            ----enterprise_phone
            ----recharge_pks 充值记录的id字符串,逗号拼接
        """
        db.session.commit()
        bill = Bill()
        bill.headline = headline
        bill.headline_type = headline_type
        bill.email = email
        if bill_no:
            bill.bill_no = bill_no
        if bank_name:
            bill.bank_name = bank_name
        if bank_account:
            bill.bank_account = bank_account
        if enterprise_name:
            bill.enterprise_name = enterprise_name
        if enterprise_address:
            bill.enterprise_address = enterprise_address
        if enterprise_phone:
            bill.enterprise_phone = enterprise_phone
        bill.pub_date = datetime.now()
        bill.status = 1         # 待开票
        bill.user_id = user_id
        bill.company_id = 1     # 无感行

        amounts = Decimal(str(0.0))
        for row in recharge_pks.split(","):
            recharge = Recharge.query.filter(Recharge.id == row).first()
            amounts += recharge.amount

        try:
            bill.amounts = amounts
            db.session.add(bill)
            db.session.flush()
            new_id = bill.id

            for row in recharge_pks.split(","):
                bill_detail = BillDetail()
                bill_detail.bill_id = new_id
                bill_detail.recharge_id = row
                bill_detail.company_id = 1  # 无感行
                db.session.add(bill_detail)

            db.session.commit()
            return {'id': new_id}
        except SQLAlchemyError:
            import traceback
            print traceback.format_exc()
            db.session.rollback()
            return -2
        finally:
            db.session.close()
