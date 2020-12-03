# coding:utf-8
from collections import defaultdict
from database.db import db
from database.Order import Order
from database.UserProfile import UserProfile
from database.Company import Company
from database.BusRoute import BusRoute
from database.BusStation import BusStation


class OrderService(object):

    @staticmethod
    def order_list(company_id, mobile, offset, limit):
        query = db.session.query(Order, UserProfile, Company, BusRoute).join(
            UserProfile, UserProfile.id == Order.user_id).join(
            Company, Company.id == Order.company_id).join(
            BusRoute, BusRoute.id == Order.route_id).filter(
            Order.company_id == company_id)
        if mobile:
            query = query.filter(UserProfile.mobile == mobile)
        query = query.order_by(Order.id.desc())
        count = query.count()
        sets = query.offset(offset).limit(limit).all()
        results = []
        for row in sets:
            order = row[0]
            user = row[1]
            company = row[2]
            route = row[3]

            d = defaultdict()
            d['id'] = order.id
            d['amount'] = str(order.amount)
            d['bus_id'] = order.bus_id
            d['company_id'] = order.company_id
            d['company_name'] = company.name
            d['content'] = order.content
            d['create_time'] = company.create_time.strftime('%Y-%m-%d %H:%M:%S')
            d['discount'] = str(order.discount)
            d['discount_way'] = order.discount_way
            d['order_no'] = order.order_no
            d['pay_time'] = order.pay_time.strftime('%Y-%m-%d %H:%M:%S')
            d['pay_type'] = order.pay_type
            d['real_amount'] = str(order.real_amount)
            d['route_name'] = route.line_no
            d['scan_time'] = order.scan_time.strftime('%Y-%m-%d %H:%M:%S')
            d['status'] = order.status
            d['station_id'] = order.station_id
            if order.station_id:
                station = db.session.query(BusStation).filter(
                    BusStation.id == order.station_id).first()
                if station:
                    d['station_name'] = station.name
            d['user_id'] = order.user_id
            d['user_mobile'] = user.mobile
            d['user_nickname'] = user.nickname
            d['verify_type'] = order.verify_type
            results.append(d)
        return {'count': count, 'results': results}
