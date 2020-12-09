# coding:utf-8
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from database.BusRoute import BusRoute
from database.Company import Company


class BusRouteService(object):

    @staticmethod
    def route_list(company_id, line_no, offset, limit):
        db.session.commit()
        query = db.session.query(BusRoute)
        if line_no:
            query = query.filter(BusRoute.line_no == line_no)

        query = query.filter(BusRoute.company_id == company_id)
        count = query.count()
        sets = query.offset(offset).limit(limit).all()
        results = []
        company = Company.query.filter(
            Company.id == company_id).first()
        for bus_route in sets:
            d = defaultdict()
            d['company'] = bus_route.company_id
            d['company_name'] = company.name
            d['end_time'] = bus_route.end_time
            d['start_time'] = bus_route.end_time
            d['fees'] = str(bus_route.fees)
            d['id'] = bus_route.id
            d['line_no'] = bus_route.line_no
            d['status'] = bus_route.status
            d['status_name'] = u'启用' if bus_route.status == 1 else u'禁用'
            results.append(d)
        return {'count': count, 'results': results}

    @staticmethod
    def route_add(company_id, start_time, end_time, fees, line_no):
        db.session.commit()
        bus_route = BusRoute()
        bus_route.start_time = start_time
        bus_route.end_time = end_time
        bus_route.fees = fees
        bus_route.line_no = line_no
        bus_route.status = 1    # 启用
        bus_route.company_id = company_id
        db.session.add(bus_route)
        db.session.flush()
        new_id = bus_route.id
        try:
            db.session.commit()
            return new_id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def route_update(pk, start_time, end_time, fees, line_no):
        db.session.commit()
        route = db.session.query(BusRoute).filter(BusRoute.id == pk).first()
        if not route:
            return -1
        if start_time:
            route.start_time = start_time
        if end_time:
            route.end_time = end_time
        if fees:
            route.fees = fees
        if line_no:
            route.line_no = line_no
        try:
            db.session.commit()
            return pk
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def route_disable(pk):
        db.session.commit()
        route = db.session.query(BusRoute).filter(BusRoute.id == pk).first()
        if not route:
            return -1
        if route.status != 1:
            return -3
        route.status = 2
        try:
            db.session.commit()
            return pk
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def route_enable(pk):
        db.session.commit()
        route = db.session.query(BusRoute).filter(BusRoute.id == pk).first()
        if not route:
            return -1
        if route.status != 2:
            return -3
        route.status = 1
        try:
            db.session.commit()
            return pk
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
