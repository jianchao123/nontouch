# coding:utf-8
try:
    import time
    import json
    from datetime import datetime
    from decimal import Decimal
    from sqlalchemy import func
    from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
    from sqlalchemy.exc import SQLAlchemyError
    from database.db import db
    from database.AdminUser import AdminUser
    from database.UserPermissions import UserPermissions
    from database.Permissions import Permissions
    from database.Recharge import Recharge
    from database.UserProfile import UserProfile
    from collections import defaultdict
    from ext import cache
except:
    import traceback
    print traceback.format_exc()


class UserProfileService(object):
    TOKEN_ID_KEY = 'hash:token.id:{}'
    INVALID_USER_ID = -1
    USER_OPERATIONS = 'user:operations:{}'

    @staticmethod
    def token_to_id(token):
        """
        根据用户token获取用户id

        args:
            token: token字符串

        return:
            int. UserId
        """
        user_id = cache.get(UserProfileService.TOKEN_ID_KEY.format(token))
        return int(user_id) if user_id else UserProfileService.INVALID_USER_ID

    @staticmethod
    def get_user_permissions(user_id):
        """获取当前登录用户的所有权限功能"""

        # cache_key = UserProfileService.USER_OPERATIONS.format(user_id)
        # user_operations = cache.get(cache_key)
        # if not user_operations:
        #     user_info = defaultdict()
        #     admin_user = db.session.query(AdminUser).filter(
        #         AdminUser.id == user_id).first()
        #     user_info['company_id'] = admin_user.company_id
        #     permissions = db.session.query(Permissions).join(
        #         UserPermissions,
        #         UserPermissions.permission_id == Permissions.id).filter(
        #         UserPermissions.user_id == user_id)
        #
        #     results = []
        #     for row in permissions:
        #         d = defaultdict()
        #         d['id'] = row.id
        #         d['permission_name'] = row.permission_name
        #         d['method'] = row.method
        #         d['url'] = row.url
        #         d['entity_classes'] = row.entity_classes
        #         results.append(d)
        #     user_info['permissions'] = results
        #     cache.set(cache_key, json.dumps(user_info))
        #     cache.expire(cache_key, 5)
        # else:
        #     user_info = json.loads(user_operations)

        user_info = defaultdict()
        admin_user = db.session.query(AdminUser).filter(
            AdminUser.id == user_id).first()
        user_info['company_id'] = admin_user.company_id
        permissions = db.session.query(Permissions).join(
            UserPermissions,
            UserPermissions.permission_id == Permissions.id).filter(
            UserPermissions.user_id == user_id)

        results = []
        for row in permissions:
            d = defaultdict()
            d['id'] = row.id
            d['permission_name'] = row.permission_name
            d['method'] = row.method
            d['url'] = row.url
            d['entity_classes'] = row.entity_classes
            results.append(d)
        user_info['permissions'] = results
        return user_info

    def get_entity_record(self, entity_class, pk):
        try:
            obj = db.session.query(entity_class).filter(
                entity_class.id == pk).one()
            return obj
        except (NoResultFound, MultipleResultsFound):
            return None

    @staticmethod
    def app_user_list(company_id, mobile, offset, limit):
        """APP用户列表"""
        query = db.session.query(UserProfile).filter(
            UserProfile.company_id == company_id)
        if mobile:
            query = query.filter(UserProfile.mobile == mobile)
        count = query.with_entities(func.count(UserProfile.id)).scalar()
        sets = query.order_by(UserProfile.id.desc()).offset(
            offset).limit(limit).all()
        results = []

        for row in sets:
            # 子账户
            sub_accounts = []
            from database.FaceImg import FaceImg
            from database.UserCoupe import UserCoupe

            faces = db.session.query(FaceImg).filter(FaceImg.parent_mobile == mobile)
            for face in faces:
                sub_accounts.append({
                    "sub_account_mobile": face.baidu_user_id,
                    "sub_account_name": face.sub_account_name,
                    "oss_url": face.oss_url
                })

            user_coupes = []
            user_coupe_set = db.session.query(UserCoupe).filter(
                UserCoupe.user_id == row.id)
            for user_coupon in user_coupe_set:
                coupon = user_coupon.coupon
                user_coupes.append({
                    "face_value": str(coupon.face_value),
                    "code": coupon.code
                })

            results.append({
                'id': row.id,
                'nickname': row.nickname,
                'mobile': row.mobile,
                'id_card': row.id_card,
                'email': row.email,
                'level': 'APP用户',
                'balance': str(row.balance),
                'date_joined': row.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                'is_active': row.is_active,
                'username': row.username,
                'sub_account': sub_accounts,
                'coupons': user_coupes
            })
        return {'count': count, "results": results}

    @staticmethod
    def app_user_update(pk, company_id, is_active, balance):
        """修改APP用户"""
        user = db.session.query(UserProfile).filter(
            UserProfile.id == pk).first()
        if not user:
            return -1

        try:
            if is_active != None:
                print is_active
                user.is_active = is_active
            if balance:
                user.balance = user.balance + Decimal(str(balance))

                recharge = Recharge()
                recharge.order_no = str(int(time.time()))
                recharge.pay_time = datetime.now()
                recharge.user_id = pk
                recharge.name = u"增加余额"
                recharge.amount = Decimal(str(balance))
                recharge.pay_type = 1   # 支付宝
                recharge.status = 2     # 成功
                recharge.remark = u"成功"
                recharge.trade_no = '123456789987654321'
                recharge.company_id = company_id

                db.session.add(recharge)
            db.session.add(user)
            db.session.commit()
            return user.id
        except SQLAlchemyError:
            import traceback
            print traceback.format_exc()
            db.session.rollback()
            return -2
        finally:
            db.session.close()

