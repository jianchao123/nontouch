# coding:utf-8
import random
import string
from Crypto.Cipher import AES
from decimal import Decimal
from datetime import datetime
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError

from database.db import db
from database.CouponType import CouponType
from database.Coupon import Coupon


class CouponTypeService(object):

    @staticmethod
    def coupon_type_list(company_id, offset, limit):
        query = db.session.query(CouponType).filter(
            CouponType.company_id == company_id).filter(CouponType.status != 10)
        count = query.count()
        sets = query.offset(offset).limit(limit)
        results = []
        for row in sets:
            d = defaultdict()
            d['id'] = row.id
            d['condition'] = row.condition
            d['content'] = row.content
            d['face_value'] = str(row.face_value)
            d['give_out_begin_time'] = row.give_out_begin_time.strftime(
                '%Y-%m-%d %H:%M:%S')
            d['give_out_end_time'] = row.give_out_end_time.strftime(
                '%Y-%m-%d %H:%M:%S')
            d['img_url'] = row.img_url
            d['is_online'] = row.is_online
            d['link'] = row.link
            d['name'] = row.name
            d['residue_volume'] = str(row.residue_volume)
            d['status'] = row.status
            d['type'] = row.type
            d['use_begin_time'] = row.use_begin_time.strftime(
                '%Y-%m-%d %H:%M:%S')
            d['use_end_time'] = row.use_end_time.strftime('%Y-%m-%d %H:%M:%S')
            d['volume'] = str(row.volume)

            give_out_volume = row.volume - row.residue_volume
            statistics = {
                "total_volume": str(row.volume),
                "give_out_volume": give_out_volume,
                "has_been_used_volume": row.has_been_used_volume,
                "total_amount":
                    str(Decimal(str(row.volume)) * row.face_value),
                "give_out_amount":
                    str(Decimal(str(give_out_volume)) * row.face_value),
                "has_been_used_amount":
                    str(Decimal(str(row.has_been_used_volume)) * row.face_value)
            }
            d['statistics'] = statistics
            results.append(d)
        return {'count': count, 'results': results}

    @staticmethod
    def coupon_type_add(company_id, condition, content, face_value,
                        give_out_begin_time, give_out_end_time, img_url,
                        is_online, link, name,
                        use_begin_time, use_end_time, volume):
        volume = int(volume)
        try:
            if use_end_time < use_begin_time:
                return -10  # 使用结束时间应该大于使用开始时间
            if use_begin_time < give_out_end_time:
                return -11  # 使用开始时间应该大于分发结束时间
            if give_out_end_time < give_out_begin_time:
                return -12  # 分发结束时间应该大于分发开始时间
            if condition == 2 and volume % 2 != 0:
                return -13  # 邀请新用户领取优惠券活动,数量必须为偶数
            if condition == 2:
                # 1, "未开始"), (2, "活动中"), (3, "活动结束"), (10, "删除"
                count = CouponType.query.filter(
                    CouponType.condition == 2,
                    CouponType.status.in_([1, 2])).count()
                if count:
                    return -14  # 邀请新用户领取优惠券活动重复

            coupon_type = CouponType()
            coupon_type.condition = condition
            coupon_type.content = content
            coupon_type.face_value = face_value
            coupon_type.give_out_begin_time = \
                datetime.strptime(give_out_begin_time, '%Y-%m-%d %H:%M:%S')
            coupon_type.give_out_end_time = \
                datetime.strptime(give_out_end_time, '%Y-%m-%d %H:%M:%S')
            coupon_type.img_url = img_url
            coupon_type.is_online = is_online
            coupon_type.link = link
            coupon_type.name = name
            coupon_type.type = 1  # 抵扣金额
            coupon_type.use_begin_time = \
                datetime.strptime(use_begin_time, '%Y-%m-%d %H:%M:%S')
            coupon_type.use_end_time = \
                datetime.strptime(use_end_time, '%Y-%m-%d %H:%M:%S')
            coupon_type.volume = volume
            coupon_type.company_id = company_id
            coupon_type.residue_volume = volume
            coupon_type.status = 1
            coupon_type.has_been_used_volume = 0
            db.session.add(coupon_type)
            db.session.flush()

            # 为活动生成优惠券
            coupons = []
            for _ in range(volume):
                coupon = Coupon()
                chars = string.ascii_letters + string.digits
                coupon.code = ''.join(
                    [random.choice(chars) for i in range(AES.block_size)])
                coupon.face_value = face_value
                coupon.status = 1  # 未发放
                coupon.use_begin_time = coupon_type.use_begin_time
                coupon.use_end_time = coupon_type.use_end_time
                coupon.type_id = coupon_type.id
                coupon.company_id = company_id   # 无感行 应该为1
                coupons.append(coupon)
            db.session.add_all(coupons)
            db.session.commit()
        except SQLAlchemyError:
            import traceback
            print traceback.format_exc()
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def coupon_type_change(pk, content, img_url, is_online, link, name):
        coupon_type = CouponType.query.filter(
            CouponType.id == pk).first()
        if not coupon_type:
            return -1
        coupon_type.content = content
        coupon_type.img_url = img_url
        coupon_type.is_online = is_online   # 活动上线或者下线
        coupon_type.link = link
        coupon_type.name = name
        coupon_type.type = 1  # 抵扣金额
        db.session.add(coupon_type)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def offline(pk):
        """
        下线活动
        下线活动只是不能继续发放优惠券了,已发放的优惠券还是可以继续使用
        """
        coupon_type = db.session.query(CouponType).filter(
            CouponType.id == pk).first()
        if not coupon_type:
            return -1
        if coupon_type.is_online != 1:
            return -2
        if coupon_type.status not in (1, 2):
            return -3
        coupon_type.is_online = 0       # 下线
        coupon_type.status = 3          # 活动结束
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
        finally:
            db.session.close()

    @staticmethod
    def delete_coupon_type(pk):
        """
        删除活动
        删除活动并不删除这次活动发放的券码,券码还是有效且可以使用
        """
        coupon_type = db.session.query(CouponType).filter(
            CouponType.id == pk).first()
        if not coupon_type:
            return -1
        if coupon_type.status == 2:    # 活动中,不能删除
            return -2
        coupon_type.status = 10
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return -3
        finally:
            db.session.close()