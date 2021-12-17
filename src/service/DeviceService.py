# coding:utf-8
from datetime import datetime
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError

from database.db import db
from database.BusCar import BusCar
from database.IotDevice import IotDevice


class DeviceService(object):

    @staticmethod
    def device_list(company_id, car_no, device_no, offset, limit):
        db.session.commit()
        query = db.session.query(IotDevice, BusCar.bus_id).join(
            BusCar, BusCar.id == IotDevice.car_id, isouter=True)
        query = query.filter(IotDevice.status != 10)
        if car_no:
            query = query.filter(BusCar.bus_id == car_no)
        if device_no:
            query = query.filter(IotDevice.device_no == device_no)

        query = query.filter(IotDevice.company_id == company_id)
        count = query.count()
        sets = query.offset(offset).limit(limit).all()
        results = []

        for row, bus_id in sets:
            d = defaultdict()
            d['id'] = row.id
            d['device_name'] = row.device_name
            d['mac'] = row.mac
            d['version_no'] = row.version_no
            d['device_iid'] = row.device_iid
            d['imei'] = row.imei
            d['status'] = row.status
            d['sound_volume'] = row.sound_volume
            d['device_type'] = row.device_type
            d['license_plate_number'] = row.license_plate_number
            results.append(d)
        return {'count': count, 'results': results}

    @staticmethod
    def binding_car(car_id, pk):
        db.session.commit()
        car = BusCar.query.filter(BusCar.id == car_id).first()
        if not car:
            return -10

        device = db.session.query(IotDevice).filter(
            IotDevice.id == pk).first()
        if not device:
            return -1
        if device.status != 1:
            return -3

        # 该车辆是否已经绑定设备
        if db.session.query(IotDevice).filter(
                IotDevice.car_id == car_id).first():
            return -4
        car = db.session.query(BusCar).filter(
            BusCar.id == car_id).first()

        # 如果用户关联设备和车辆,判断状态是否为1,为1就修改到2
        if device.status == 1:
            device.status = 2
        try:
            device.status = 3   # 已绑车
            device.car_id = car.id
            device.license_plate_number = car.bus_id
            db.session.commit()
            return device.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def disable_binding(pk):
        """
        解除绑定
        """
        db.session.commit()
        device = db.session.query(IotDevice).filter(
            IotDevice.id == pk).first()
        if not device:
            return -1
        if device.status != 3:
            return -3
        try:
            device.status = 2  # 已分配,未绑车
            device.car_id = None
            device.license_plate_number = ""
            db.session.commit()
            return device.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def device_update(pk, sound_volume, device_type):
        db.session.commit()  # SELECT
        device = db.session.query(IotDevice).filter(
            IotDevice.id == pk).first()
        if not device:
            return -1
        if sound_volume:
            device.sound_volume = sound_volume

        if device_type:
            device.device_type = device_type
        # if car_id:
        #     # 清空
        #     if car_id == -10:
        #         device.car_id = None
        #         device.license_plate_number = None
        #     else:
        #         # 该车辆是否已经绑定设备
        #         if db.session.query(IotDevice).filter(
        #                 IotDevice.car_id == car_id).first():
        #             return -2
        #         car = db.session.query(BusCar).filter(
        #             BusCar.id == car_id).first()
        #
        #         device.car_id = car_id
        #         device.license_plate_number = car.license_plate_number
        #         # 如果用户关联设备和车辆,判断状态是否为1,为1就修改到2
        #         if device.status == 1:
        #             device.status = 2

        try:
            d = {'id': device.id}
            db.session.commit()
            return d
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
