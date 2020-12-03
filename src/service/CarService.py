# coding:utf-8
from datetime import datetime
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError

from database.db import db
from database.BusCar import BusCar
from database.Company import Company
from database.BusRoute import BusRoute
from database.Device import Device


class CarService(object):

    @staticmethod
    def car_list(company_id, bus_id, not_binding, offset, limit):
        """
        车辆列表
        """
        company = db.session.query(Company).filter(
            Company.id == company_id).first()

        query = db.session.query(BusCar).filter(
            BusCar.company_id == company_id)
        if bus_id:
            query = query.filter(BusCar.bus_id == bus_id)
        if not_binding:
            # 获取该公司已绑定设备的车辆id
            devices = db.session.query(Device).filter(
                Device.company_id == company_id, Device.status == 2).all()
            car_ids = [row.car_id for row in devices]
            query = query.filter(BusCar.id.notin_(car_ids))
        count = query.count()
        sets = query.offset(offset).limit(limit).all()

        results = []
        for car in sets:
            d = defaultdict()
            d['id'] = car.id
            d['brand'] = car.brand
            d['bus_id'] = car.bus_id
            d['bus_load'] = car.bus_load
            d['buy_date'] = car.buy_date.strftime('%Y-%m-%d')
            d['chassis'] = car.chassis
            d['company'] = car.company_id
            d['company_name'] = company.name
            d['engine'] = car.engine
            d['load'] = car.load
            d['model_number'] = car.model_number
            d['product_date'] = car.product_date.strftime('%Y-%m-%d')
            d['status'] = car.status  # 1未绑线 2已绑线
            d['type'] = car.type
            d['is_binding'] = 1 if car.status == 3 else 0
            d['route_id'] = car.route_id
            d['is_servicing'] = car.is_servicing
            if car.route_id:
                route = db.session.query(BusRoute).filter(
                    BusRoute.id == car.route_id).first()
                d['line_no'] = route.line_no
            results.append(d)
        return {'count': count, 'results': results}

    @staticmethod
    def car_add(company_id, brand, bus_id, bus_load, buy_date,
                chassis, engine, load, model_number, product_date,
                type, is_servicing):
        car = BusCar()
        car.brand = brand
        car.bus_id = bus_id
        car.bus_load = bus_load
        car.buy_date = datetime.strptime(buy_date, '%Y-%m-%d').date()
        car.chassis = chassis
        car.engine = engine
        car.load = load
        car.model_number = model_number
        car.product_date = datetime.strptime(product_date, '%Y-%m-%d').date()
        car.company_id = company_id
        car.status = 1  # 未绑线路
        car.type = type
        car.is_servicing = is_servicing
        try:
            db.session.add(car)
            db.session.flush()
            new_id = car.id

            db.session.commit()
            return new_id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def car_update(pk, brand, bus_id, bus_load,
                   buy_date, chassis, engine, load,
                   model_number, product_date,
                   type, is_servicing):
        car = db.session.query(BusCar).filter(BusCar.id == pk).first()
        if not car:
            return -1
        car.brand = brand
        car.bus_id = bus_id
        car.bus_load = bus_load
        car.buy_date = datetime.strptime(buy_date, '%Y-%m-%d').date()
        car.chassis = chassis
        car.engine = engine
        car.load = load
        car.model_number = model_number
        car.product_date = datetime.strptime(product_date, '%Y-%m-%d').date()
        car.type = type
        car.is_servicing = is_servicing
        try:
            db.session.commit()
            return pk
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def car_binding(pk, route_id):
        """
        绑定线路
        :param pk:
        :param route_id:
        :return:
        """
        car = db.session.query(BusCar).filter(BusCar.id == pk).first()
        if not car:
            return -1
        if car.status != 1: # 不是未绑线状态
            return -3
        route = BusRoute.query.filter(BusRoute.id == route_id).first()
        if route.status == 2:   # 线路已经禁用
            return -4
        car.status = 2  # 已绑线
        car.route_id = route_id
        try:
            db.session.commit()
            return pk
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def car_unbinding(pk):
        car = db.session.query(BusCar).filter(BusCar.id == pk).first()
        if not car:
            return -1
        if car.status != 2:
            return -3

        car.status = 1  # 未绑线
        car.route_id = None
        try:
            db.session.commit()
            return pk
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
