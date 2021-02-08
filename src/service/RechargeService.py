# coding:utf-8
from collections import defaultdict
from sqlalchemy import or_
from database.db import db
from database.Recharge import Recharge
from database.UserProfile import UserProfile


class RechargeService(object):

    @staticmethod
    def recharge_list(company_id, find_str, pay_type, status, offset, limit, user_id):
        db.session.commit()
        query = db.session.query(Recharge, UserProfile.username).join(
            UserProfile, UserProfile.id == Recharge.user_id).filter(
            Recharge.company_id == company_id)
        if find_str:
            query = query.filter(or_(Recharge.order_no == find_str,
                                     UserProfile.mobile == find_str))
        if pay_type:
            query = query.filter(Recharge.pay_type == pay_type)
        if status:
            query = query.filter(Recharge.status == status)
        if user_id:
            query = query.filter(Recharge.user_id == user_id)
        count = query.count()
        sets = query.order_by(Recharge.id.desc()).offset(offset).limit(limit)
        results = []
        for row in sets:
            recharge = row[0]
            d = defaultdict()
            d['id'] = recharge.id
            d['amount'] = str(recharge.amount)
            d['body'] = recharge.body
            d['create_time'] = recharge.create_time.strftime('%Y-%m-%d %H:%M:%S')
            d['name'] = recharge.name
            d['order_no'] = recharge.order_no
            d['pay_time'] = recharge.pay_time.strftime('%Y-%m-%d %H:%M:%S')
            d['pay_type'] = recharge.pay_type
            d['remark'] = recharge.remark
            d['status'] = recharge.status
            d['trade_no'] = recharge.trade_no
            d['user_id'] = recharge.user_id
            d['username'] = row[1]
            results.append(d)
        return {'count': count, 'results': results}
