# coding:utf-8
from datetime import datetime
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError

from database.db import db
from database.BusCar import BusCar
from database.Device import Device


class DeviceService(object):

    @staticmethod
    def device_list(company_id, car_no, device_no, offset, limit):

        query = db.session.query(Device, BusCar.bus_id).join(
            BusCar, BusCar.id == Device.car_id, isouter=True)
        if car_no:
            query = query.filter(BusCar.bus_id == car_no)
        if device_no:
            query = query.filter(Device.device_no == device_no)

        query = query.filter(Device.company_id == company_id)
        count = query.count()
        sets = query.offset(offset).limit(limit).all()
        results = []
        for row, bus_id in sets:
            d = defaultdict()
            d['id'] = row.id
            d['brand'] = row.brand
            d['model_number'] = row.model_number
            d['type'] = row.type
            d['pro_seq_number'] = row.pro_seq_number
            d['device_no'] = row.device_no
            d['manufacture_date'] = \
                row.manufacture_date.strftime('%Y-%m-%d')
            d['buy_date'] = row.buy_date.strftime('%Y-%m-%d')
            d['car'] = bus_id
            d['is_online'] = row.is_online
            d['status'] = row.status
            results.append(d)
        return {'count': count, 'results': results}

    @staticmethod
    def device_add(company_id, brand, buy_date, device_no,
                   manufacture_date, model_number, name, pro_seq_number,
                   type):
        device = Device()
        device.brand = brand
        device.name = name
        device.type = type
        device.status = 2
        device.model_number = model_number
        device.pro_seq_number = pro_seq_number
        device.device_no = device_no
        device.manufacture_date = datetime.strptime(
            manufacture_date, '%Y-%m-%d').date()
        device.buy_date = datetime.strptime(
            buy_date, '%Y-%m-%d').date()
        device.company_id = company_id
        device.is_online = 1

        try:
            db.session.add(device)
            db.session.flush()
            new_id = device.id
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
        return new_id

    @staticmethod
    def binding_car(car_id, pk):

        device = db.session.query(Device).filter(
            Device.id == pk).first()
        if not device:
            return -1
        if device.status != 2:
            return -3
        try:
            device.status = 3   # 已绑车
            device.car_id = car_id
            db.session.commit()
            return device.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def unbinding_car(pk):
        """
        解除绑定
        """

        device = db.session.query(Device).filter(
            Device.id == pk).first()
        if not device:
            return -1
        if device.status != 3:
            return -3
        try:
            device.status = 2  # 已分配,未绑车
            device.car_id = None
            db.session.commit()
            return device.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def device_update(pk, brand, buy_date, device_no, manufacture_date,
                      model_number, name, pro_seq_number,
                      type):
        device = db.session.query(Device).filter(Device.id == pk).first()
        if not device:
            return -1
        try:
            if brand:
                device.brand = brand
            if buy_date:
                device.buy_date = datetime.strptime(
                    buy_date, '%Y-%m-%d').date()
            if device_no:
                device.device_no = device_no
            if manufacture_date:
                device.manufacture_date = datetime.strptime(
                    manufacture_date, '%Y-%m-%d').date()
            if model_number:
                device.model_number = model_number
            if name:
                device.name = name
            if pro_seq_number:
                device.pro_seq_number = pro_seq_number
            if type:
                device.type = type
            db.session.add(device)
            db.session.commit()
            return pk
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
