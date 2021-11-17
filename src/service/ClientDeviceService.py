# coding:utf-8
import json
import struct
import requests
from datetime import date
from datetime import timedelta

from database.db import db
from database.Device import Device
from database.BusCar import BusCar
from database.BusRoute import BusRoute
from database.PassengerWeeklyCount import PassengerWeeklyCount
from database.FaceImg import FaceImg
from ext import cache, conf


class ClientDeviceService(object):

    @staticmethod
    def get_baidu_access_token():
        access_token = cache.get('BAIDU_ACCESS_TOKEN')
        d = {
            'access_token': access_token,
            'group_id': conf.config['BAIDU_GROUP_ID'],
        }
        return d

    @staticmethod
    def get_device_info(device_no):
        db.session.commit()
        device = db.session.query(Device).filter(
            Device.device_no == device_no).first()
        if not device:
            return -1
        if device.status != 3:
            return -10
        car_id = device.car_id
        car = db.session.query(BusCar).filter(BusCar.id == car_id).first()
        route = db.session.query(BusRoute).filter(
            BusRoute.id == car.route_id).first()
        if not route:
            return -11
        return {"fees": str(route.fees)}

    @staticmethod
    def device_update_strategy(device_no, data):
        db.session.commit()
        fid_dict = {}
        length = len(data)
        offset = 0
        while offset < length:
            s = data[offset: offset + 8]
            ret_all = struct.unpack('<Ii', s)
            fid = ret_all[0]
            feature_crc = ret_all[1]
            fid_dict[fid] = feature_crc
            offset += 8

        device_fid_list = fid_dict.keys()

        # 该条线路的fids
        device = Device.query.filter(Device.device_no == device_no).first()
        if not device:
            return -1
        if device.status != 3:
            return -10
        car = BusCar.query.filter(BusCar.id == device.car_id).first()
        route = BusRoute.query.filter(BusRoute.id == car.route_id).first()
        if not route:
            return -11
        pwc_results = PassengerWeeklyCount.query.filter(
            PassengerWeeklyCount.route_id == route.id).all()
        line_fid_list = [row.fid for row in pwc_results]

        # 增加 删除 更新
        add_list = list(set(line_fid_list) - set(device_fid_list))
        delete_list = list(set(device_fid_list) - set(line_fid_list))
        intersection = list(set(device_fid_list) & set(line_fid_list))  # 交集

        line_dict = {}
        faces = FaceImg.query.filter(
            FaceImg.id.in_(intersection)).all()
        for row in faces:
            line_dict[row.id] = row.feature_crc

        update_list = []
        for fid in intersection:
            if fid_dict[fid] != line_dict[fid]:
                update_list.append(fid)

        results = db.session.query(FaceImg).filter(
            FaceImg.id.in_(add_list)).all()
        add = []
        for row in results:
            add.append({"fid": row.id, "feature": row.feature})

        results = db.session.query(FaceImg).filter(
            FaceImg.id.in_(delete_list)).all()
        delete = []
        for row in results:
            delete.append({"fid": row.id})

        results = db.session.query(FaceImg).filter(
            FaceImg.id.in_(update_list)).all()
        update = []
        for row in results:
            update.append({"fid": row.id, "feature": row.feature})

        data = {
            "add": add,
            "delete": delete,
            "update": update
        }
        return data


    # @staticmethod
    # def device_update_strategy(mobiles, device_no):
    #     db.session.commit()
    #     device_mobile_list = mobiles.split(",") if mobiles else []
    #     yesterday = date.today() - timedelta(days=1)
    #     device = Device.query.filter(Device.device_no == device_no).first()
    #     if not device:
    #         return -1
    #     if device.status != 3:
    #         return -10
    #     car = BusCar.query.filter(BusCar.id == device.car_id).first()
    #     route = BusRoute.query.filter(BusRoute.id == car.route_id).first()
    #     if not route:
    #         return -11
    #
    #     server_mobile_list = PassengerWeeklyCount.query.filter(
    #         PassengerWeeklyCount.route_id == route.id).all()
    #     server_mobile_list = [row.mobile for row in server_mobile_list]
    #     print(server_mobile_list, device_mobile_list)
    #     add_list = list(set(server_mobile_list) - set(device_mobile_list))
    #     delete_list = list(set(device_mobile_list) - set(server_mobile_list))
    #     upgrade_list = list(set(server_mobile_list) & set(device_mobile_list))  # 交集
    #     print(upgrade_list)
    #
    #     # 升级的
    #     upgrade = []
    #     if upgrade_list:
    #         # 昨天更新的人脸
    #         face_images = FaceImg.query.filter(
    #             FaceImg.baidu_user_id.in_(upgrade_list),
    #             db.cast(FaceImg.face_last_time, db.DATE) == yesterday).all()
    #         for row in face_images:
    #             upgrade.append({
    #                 "mobile": row.baidu_user_id,
    #                 "oss_url": row.oss_url
    #             })
    #
    #     # 新增的
    #     add = []
    #     face_images = FaceImg.query.filter(
    #         FaceImg.baidu_user_id.in_(add_list)).all()
    #     for row in face_images:
    #         add.append({
    #             "mobile": row.baidu_user_id,
    #             "oss_url": row.oss_url
    #         })
    #
    #     data = {
    #         "add": add,
    #         "delete": delete_list,
    #         "upgrade": upgrade
    #     }
    #     return data
