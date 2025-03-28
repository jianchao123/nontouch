# coding:utf-8
from collections import defaultdict
from database.db import db
from database.Coupon import Coupon
from database.UserCoupe import UserCoupe
from database.UserProfile import UserProfile
from database.CouponType import CouponType


class CouponService(object):

    @staticmethod
    def coupon_list(mobile, type_id, offset, limit):
        db.session.commit()
        query = db.session.query(Coupon, CouponType.name).join(
            CouponType, CouponType.id == Coupon.type_id)
        if type_id:
            query = query.filter(Coupon.type_id == type_id)
        if mobile:
            user_results = db.session.query(UserProfile).filter(
                UserProfile.mobile.like('%%{}%%'.format(mobile)))
            userids = [row.id for row in user_results]
            user_coupe_results = db.session.query(
                UserCoupe).filter(UserCoupe.user_id.in_(userids))
            coupon_ids = [row.coupon_id for row in user_coupe_results]
            query = query.filter(Coupon.id.in_(coupon_ids))
        count = query.count()
        sets = query.offset(offset).limit(limit)
        results = []
        for row in sets:
            coupon = row[0]
            coupon_type_name = row[1]

            d = defaultdict()
            if coupon.status in (2, 3, 4):
                objs = db.session.query(UserCoupe, UserProfile).join(
                    UserProfile, UserProfile.id == UserCoupe.user_id).filter(
                    UserCoupe.coupon_id == coupon.id).first()
                user_coupe = objs[0]
                user = objs[1]
                d['get_time'] = user_coupe.get_time.strftime(
                    '%Y-%m-%d %H:%M:%S')
                if user_coupe.use_time:
                    d['use_time'] = user_coupe.use_time.strftime(
                        '%Y-%m-%d %H:%M:%S')
                d['nickname'] = user.nickname
            d['id'] = coupon.id
            d['code'] = coupon.code
            d['face_value'] = str(coupon.face_value)
            d['name'] = coupon_type_name
            d['status'] = coupon.status
            print coupon.status
            if coupon.status in (2, 3, 4):
                user_profile = db.session.query(UserProfile).join(
                    UserCoupe, UserCoupe.user_id == UserProfile.id).filter(
                    UserCoupe.coupon_id == coupon.id).first()
                d['mobile'] = user_profile.mobile
            else:
                d['mobile'] = ""

            results.append(d)
        return {'count': count, 'results': results}
