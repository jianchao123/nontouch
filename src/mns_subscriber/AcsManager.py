# coding:utf-8
import os
import sys
import zlib
import time
import json
import base64
import struct
import inspect
from datetime import datetime
from collections import defaultdict

from aliyunsdkcore.client import AcsClient
from aliyunsdkiot.request.v20180120.RegisterDeviceRequest import \
    RegisterDeviceRequest
from aliyunsdkiot.request.v20180120.PubRequest import PubRequest

from define import RedisKey, classes, grade
import db


filename = inspect.getframeinfo(inspect.currentframe()).filename
project_dir = os.path.dirname(os.path.realpath(filename))
project_dir = os.path.dirname(project_dir)
sys.path.append(project_dir)
from msgqueue import producer
import utils


class AcsManager(object):
    """注册设备"""

    def __init__(self, product_key, mns_access_key_id,
                 mns_access_key_secret, oss_domain,
                 oss_access_key_id, oss_key_secret):
        self.client = AcsClient(mns_access_key_id,
                                mns_access_key_secret, 'cn-shanghai')
        self.product_key = product_key
        self.oss_domain = oss_domain
        self.oss_access_key_id = oss_access_key_id
        self.oss_key_secret = oss_key_secret

    def _upgrade_version(self, device_name):
        """升级版本"""
        self._send_device_msg(device_name, RedisKey.UPGRADE_JSON)

    def _set_oss_info(self, device_name):
        """设置oss信息"""
        jdata = {
            "cmd": "ossinfo",
            "ossdomain": self.oss_domain,
            "osskeyid": self.oss_access_key_id,
            "osskeysecret": self.oss_key_secret[12:] + self.oss_key_secret[:12]
        }
        self._send_device_msg(device_name, jdata)

    def _send_device_msg(self, devname, jdata):
        request = PubRequest()
        request.set_accept_format('json')

        topic = '/' + self.product_key + '/' + devname + '/user/get'
        request.set_TopicFullName(topic)

        message = json.dumps(jdata, encoding="utf-8")
        message = base64.b64encode(message)
        request.set_MessageContent(message)
        request.set_ProductKey(self.product_key)
        # request.set_Qos("Qos")

        response = self.client.do_action_with_exception(request)
        return json.loads(response)

    def _set_workmode(self, device_name, workmode, chepai,
                      cur_volume, person_limit):
        """
        设置设备工作模式 0车载 1通道闸口 3注册模式
        :param device_name:
        :param workmode:
        :param cur_volume:
        :return:
        """
        if workmode not in [0, 1, 3]:
            return -1
        if not cur_volume:
            cur_volume = 6

        jdata = {
            "cmd": "syntime",
            "time": int(time.time()),
            "chepai": chepai.encode('utf8'),
            "workmode": workmode,
            "delayoff": 7,
            "leftdetect": 2,
            "jiange": 10,
            "cleartime": 70,
            "shxmode": 0,
            "volume": int(cur_volume),
            "facesize": 390,
            "uploadtype": 1,
            "natstatus": 0,
            "timezone": 8,
            "temperature": 0,
            "noreg": 0,
            "light_type": 0,
            "person_limit": int(person_limit)
        }
        return self._send_device_msg(device_name, jdata)

    @staticmethod
    def _jwd_swap(a):
        du = int(a / 100)

        fen = int(a - du * 100)
        miao = (a - du * 100 - fen) * 60
        return du + fen / 60.0 + miao / 3600.0

    @staticmethod
    def check_cur_stream_no(device_name, jdata):
        """检查当前stream_no"""
        if "stream_no" in jdata:
            from mns_subscriber import config
            #config.logger.error("------------stream_no----------------{}".format(str(jdata)))
            #print jdata
            rds_conn = db.rds_conn
            stream_no = jdata["stream_no"]
            k = "cur_{}_stream_no".format(device_name)
            rds_stream_no = rds_conn.get(k)
            if rds_stream_no and str(rds_stream_no) == str(stream_no):
                rds_conn.delete(k)

    def add_redis_queue(self, device_name, data, pkt_cnt):
        """
        添加到redis queue
        pkt_cnt == 0表示设备上没有人员信息，但是设备也会回传一个消息
        """
        rds_conn = db.rds_conn
        if not pkt_cnt:
            self.check_person_list([], device_name)
        else:
            pkt_inx_key = '{}_pkt_inx'.format(device_name)
            raw_queue_key = "person_raw_" + device_name
            tt = rds_conn.incr(pkt_inx_key)
            if data:
                rds_conn.rpush(raw_queue_key, json.dumps(data))
            if int(tt) == int(pkt_cnt):
                person_list = []
                raw_data = rds_conn.lpop(raw_queue_key)
                while raw_data:
                    person_list.append(raw_data)
                    raw_data = rds_conn.lpop(raw_queue_key)
                # 删除计数key
                rds_conn.delete(pkt_inx_key)
                # 删除stream_no key,因为devwhitelist指令没有返回stream_no
                rds_conn.delete("cur_{}_stream_no".format(device_name))
                self.check_person_list(person_list, device_name)

    @staticmethod
    def get_route_id(mysql_db, mysql_cur, device_name):
        """获取线路id"""
        car_ids = []
        # 根据设备号查询线路id
        sql = "SELECT car_id FROM iot_device WHERE device_name='{}' LIMIT 1"
        iot_device = mysql_db.get(mysql_cur, sql.format(device_name))
        if not iot_device:
            return car_ids
        sql = "SELECT route_id,route_id_1 FROM bus_car WHERE id = {} LIMIT 1"
        buscar = mysql_db.get(mysql_cur, sql.format(iot_device[0]))
        if buscar[0]:
            car_ids.append(buscar[0])
        if buscar[1]:
            car_ids.append(buscar[1])
        return car_ids

    @db.transaction(is_commit=True)
    def check_person_list(self, mysql_cur, person_list, device_name):
        """
        检查人员列表
        (单设备检查人员是否需要更新)
        :return:
        """
        rds_conn = db.rds_conn
        mysql_db = db.PgsqlDbUtil
        fid_dict = {}
        for row in person_list:
            data = base64.b64decode(row)
            length = len(data)
            offset = 0
            while offset < length:
                s = data[offset: offset + 16]
                ret_all = struct.unpack('<IiiI', s)
                fid = ret_all[0]
                feature_crc = ret_all[2]
                fid_dict[str(fid)] = feature_crc
                offset += 16
        print "--------------fid_dict--------------------"
        print fid_dict
        bus_route_ids = AcsManager.get_route_id(mysql_db, mysql_cur, device_name)
        # 为空表示车辆没有绑定线路或设备没有绑定车辆
        if not bus_route_ids:
            # 清空设备所有人脸
            producer.delete_all_face(device_name)
            # 提示
            producer.update_chepai(device_name, "没有绑定车辆或线路", 6, 0, 20)
        else:
            # 根据线路ids查询fids
            device_fid_set = set(fid_dict.keys())

            sql = "SELECT fid FROM passenger_weekly_count " \
                  "WHERE route_id in ({})"
            results = mysql_db.query(
                mysql_cur, sql.format(",".join([str(x) for x in bus_route_ids])))
            face_ids = [str(row[0]) for row in results]

            add_list = list(set(face_ids) - set(device_fid_set))

            del_list = list(set(device_fid_set) - set(face_ids))

            intersection_list = list(set(face_ids) & set(device_fid_set))

            # 需要更新的feature
            update_list = []
            for row in results:
                pk = row[0]
                feature_crc = row[1]
                if str(pk) in fid_dict and str(pk) in intersection_list:
                    if feature_crc != fid_dict[str(pk)]:
                        update_list.append(str(pk))

            # 放到消息队列
            producer.device_person_update_msg(
                add_list, del_list, update_list, device_name)
            print add_list, del_list, update_list

    @db.transaction(is_commit=True)
    def create_device(self, mysql_cur, mac, shd_devid):
        """
        创建设备
        """
        from mns_subscriber import config
        rds_conn = db.rds_conn
        mysql_db = db.PgsqlDbUtil
        config.logger.info('create iot_device {} {}'.format(shd_devid, mac))

        dev_sql = "SELECT id FROM iot_device WHERE mac='{}' LIMIT 1"

        obj = mysql_db.get(mysql_cur, dev_sql.format(mac))
        if obj:
            return None

        sql = 'SELECT id,device_name FROM iot_device ' \
              'ORDER BY id DESC LIMIT 1'
        obj = mysql_db.get(mysql_cur, sql)
        if not obj:
            dev_name = 'dev_1'
        else:
            arr = obj[1].split('_')
            prefix = arr[0]
            suffix = arr[1]
            dev_name = prefix + '_' + str(int(suffix) + 1)

        # 创建设备
        request = RegisterDeviceRequest()
        request.set_accept_format('json')

        request.set_ProductKey(self.product_key)
        request.set_DeviceName(dev_name)
        response = self.client.do_action_with_exception(request)
        response = json.loads(response)
        if not response['Success']:
            config.logger.info('api create fail {}'.format(mac))
            return None
        # 添加记录
        d = {
            'device_name': response['Data']['DeviceName'],
            'status': 1,
            'mac': mac,
            'product_key': response['Data']['ProductKey'],
            'device_secret': response['Data']['DeviceSecret'],
            'sound_volume': 6,
            'license_plate_number': '',
            'company_id': 1  # 无感行 默认
        }
        mysql_db.insert(mysql_cur, d, table_name='iot_device')

        # 发布消息注册
        msg = {
            "cmd": "devid",
            "devname": response['Data']['DeviceName'],
            "productkey": response['Data']['ProductKey'],
            "devsecret": response['Data']['DeviceSecret'],
            "devicetype": 0,
            "time": int(time.time()),
            'dev_mac': mac
        }
        retd = self._send_device_msg('newdev', msg)
        config.logger.error(retd)
        rds_conn.hset(RedisKey.DEVICE_CUR_STATUS, dev_name, 1)
        rds_conn.rpush('DEVICE_NAME_QUEUE', dev_name)

        return None

    def _set_device_work_mode(self, dev_name, license_plate_number,
                              cur_volume, workmode, person_limit):
        """设置设备工作模式
        0车载 1通道闸口 3注册模式
        """
        self._set_workmode(dev_name, workmode, license_plate_number,
                           cur_volume, person_limit)

    @db.transaction(is_commit=False)
    def _init_person(self, mysql_cur, person_list, device_name):
        mysql_db = db.PgsqlDbUtil
        fid_dict = {}
        for row in person_list:
            data = base64.b64decode(row)
            length = len(data)
            offset = 0
            while offset < length:
                s = data[offset: offset + 16]
                ret_all = struct.unpack('<IiiI', s)
                fid = ret_all[0]
                feature_crc = ret_all[2]
                fid_dict[str(fid)] = feature_crc
                offset += 16

        sql = """
        SELECT f.id, f.feature_crc FROM face AS F
        INNER JOIN student AS stu ON stu.id=F.stu_id 
        WHERE F.status = 4 AND stu.status = 1 AND stu.car_id={} 
        """
        device_sql = "SELECT car_id FROM iot_device " \
                     "WHERE device_name = '{}' LIMIT 1"
        dev_car_id = mysql_db.get(mysql_cur, device_sql.format(device_name))[0]
        if dev_car_id:
            device_fid_set = set(fid_dict.keys())
            results = mysql_db.query(mysql_cur, sql.format(dev_car_id))
            face_ids = [str(row[0]) for row in results]

            add_list = list(set(face_ids) - set(device_fid_set))

            # 放到消息队列
            producer.device_person_update_msg(
                add_list, [], [], device_name)

    def check_version(self, device_name, cur_version, dev_time):
        """检查版本号"""
        from mns_subscriber import config
        #config.logger.info('----current version{}----'.format(cur_version))
        rds_conn = db.rds_conn
        all_heartbeat_val = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rds_conn.hset(RedisKey.ALL_HEARTBEAT_HASH, device_name, all_heartbeat_val)
        # 小于当前版本号就更新
        if cur_version < 1:
            self._upgrade_version(device_name)

    @db.transaction(is_commit=True)
    def _update_device(self, mysql_cur, data):
        mysql_db = db.PgsqlDbUtil
        mysql_db.update(mysql_cur, data, table_name='iot_device')

    @db.transaction(is_commit=False)
    def _get_device_info_data(self, mysql_cur, device_name):
        mysql_db = db.PgsqlDbUtil

        sql = "SELECT id,status,version_no,sound_volume," \
              "license_plate_number,device_type,person_limit" \
              " FROM iot_device WHERE device_name='{}' LIMIT 1"
        iot_device = mysql_db.get(mysql_cur, sql.format(device_name))
        return iot_device[0], iot_device[1], iot_device[2], iot_device[3], \
               iot_device[4], iot_device[5], iot_device[6]

    def init_device_params(self, device_name, shd_devid):
        """
        初始化设备参数
        """
        rds_conn = db.rds_conn

        device_status = rds_conn.hget(
            RedisKey.DEVICE_CUR_STATUS, device_name)
        # 如果没有找到这个设备直接消费掉消息
        if not device_status:
            return -10

        d = {}

        # 5表示已初始化人员
        if device_status and int(device_status) == 5:
            return 0
        pk, status, version_no, sound_volume, license_plate_number, \
            device_type, person_limit = \
            self._get_device_info_data(device_name)

        # '已创建虚拟设备'状态
        if status in [1, 2, 3, 4, 5]:
            d['device_iid'] = shd_devid

        # 设备为生成特征值设备
        if device_type == 2:
            license_plate_number = u'生成特征值专用'
            workmode = 3    # 注册模式
        else:   # device_type == 1:
            workmode = 0    # 车载模式
        # '已关联车辆'状态
        if status == 2:
            d['status'] = 3   # 已设置工作模式
            print u"设置工作模式"
            person_limit = int(person_limit) if person_limit else 40
            self._set_device_work_mode(
                device_name, license_plate_number, sound_volume,
                workmode, person_limit)
            rds_conn.hset(RedisKey.DEVICE_CUR_STATUS, device_name, 3)
        elif status == 3:       # 已设置工作模式
            d['status'] = 4     # 设置oss信息
            print u"设置oss信息"
            self._set_oss_info(device_name)
            rds_conn.hset(RedisKey.DEVICE_CUR_STATUS, device_name, 4)
        elif status == 4:       # 设置oss信息
            d['status'] = 5     # 初始人员
            d['device_iid'] = shd_devid
            print u"初始化人员"

            rds_conn.hset(RedisKey.DEVICE_CUR_STATUS, device_name, 5)
            self._init_person([], device_name)

        if d:
            d['id'] = pk
            self._update_device(d)

    @db.transaction(is_commit=False)
    def _get_sound_vol_by_name(self, mysql_cur, dev_name):
        mysql_db = db.PgsqlDbUtil
        sql = "SELECT sound_volume,car_id,device_type " \
              "FROM iot_device WHERE device_name='{}' LIMIT 1"
        chepai_sql = "SELECT license_plate_number FROM car WHERE id={} LIMIT 1"
        result = mysql_db.get(mysql_cur, sql.format(dev_name))
        car_id = result[1]
        if car_id:
            chepai = mysql_db.get(mysql_cur, chepai_sql.format(car_id))[0]
        else:
            chepai = ""
        return result[0], chepai, result[2]

    def device_rdskey_status_update(self, dev_name, cnt):
        """修改设备在redis 里的状态"""
        rds_conn = db.rds_conn
        cur_status = rds_conn.hget(RedisKey.DEVICE_CUR_STATUS, dev_name)
        if cur_status and int(cur_status) == 5:
            rds_conn.hset(RedisKey.DEVICE_CUR_PEOPLE_NUMBER, dev_name, cnt)

    def device_rebooted_setting_open_time(self, device_name, gps, ret):
        """设备重启设备开机时间"""
        rds_conn = db.rds_conn
        # 设置设备时间戳和gps
        device_timestamp = rds_conn.hget(
            RedisKey.DEVICE_CUR_TIMESTAMP, device_name)

        # 长时间关机
        if device_timestamp and \
                int(time.time()) - int(device_timestamp) > 60 * 5 and \
                (not ret):
            producer.dev_while_list(device_name)
            pk, status, version_no, sound_volume, license_plate_number, \
                device_type, person_limit = self._get_device_info_data(device_name)
            d = defaultdict()
            d['id'] = pk
            d['open_time'] = 'TO_TIMESTAMP({})'.format(int(time.time()))
            self._update_device(d)

            # 更新设备信息
            sound_vol, license_plate_number, device_type \
                = self._get_sound_vol_by_name(device_name)
            workmode = 0 if device_type == 1 else 3
            sound_vol = int(sound_vol) if sound_vol else 100
            person_limit = int(person_limit) if person_limit else 40
            producer.update_chepai(device_name, license_plate_number,
                                   sound_vol, workmode, person_limit)
            # 设置oss set
            producer.device_oss_info(device_name)

        rds_conn.hset(RedisKey.DEVICE_CUR_TIMESTAMP, device_name,
                      int(time.time()))
        if gps == ",":
            gps_str = ""
        else:
            arr = gps.split(",")
            if arr[0] and arr[1]:
                longitude = AcsManager._jwd_swap(float(arr[0]))
                latitude = AcsManager._jwd_swap(float(arr[1]))
                longitude, latitude = utils.wgs84togcj02(
                    float(longitude), float(latitude))
                gps_str = '{},{}'.format(longitude, latitude)
            else:
                gps_str = ""
        rds_conn.hset(RedisKey.DEVICE_CUR_GPS, device_name, gps_str)

    @db.transaction(is_commit=True)
    def save_imei(self, mysql_cur, device_name, imei):
        mysql_db = db.PgsqlDbUtil
        sql = "SELECT id FROM iot_device WHERE device_name='{}' LIMIT 1"
        obj = mysql_db.get(mysql_cur, sql.format(device_name))
        if obj:
            d = {
                'id': obj[0],
                'imei': imei
            }
            mysql_db.update(mysql_cur, d, table_name='iot_device')

