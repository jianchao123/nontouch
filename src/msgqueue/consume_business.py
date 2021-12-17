# coding: utf-8
import json
import time
import zlib
import base64
import requests
from datetime import datetime

from aliyunsdkcore.client import AcsClient
from aliyunsdkiot.request.v20180120.RegisterDeviceRequest import \
    RegisterDeviceRequest
from aliyunsdkiot.request.v20180120.PubRequest import PubRequest

from msgqueue import config
from msgqueue import tools
from msgqueue.db import transaction, MysqlDbUtil,rds_conn

from selenium import webdriver
import os

dir_path = os.path.dirname(__file__)
driver = webdriver.PhantomJS(executable_path=dir_path + "/phantomjs",
                             service_log_path='/data/logs/phantomjs/gh.log')


class HeartBeatConsumer(object):

    def __init__(self):
        self.logger = tools.get_logger(config.log_path)

    def heartbeat_callback(self, ch, method, properties, body):
        print "------------heartbeat-------------deliver_tag={}".\
            format(method.delivery_tag)
        # 消息确认
        ch.basic_ack(delivery_tag=method.delivery_tag)


class BusConsumer(object):

    def __init__(self):
        self.logger = tools.get_logger(config.log_path)
        self.get_station_business = GetStationBusiness(self.logger)
        self.gen_feature = GenFeature(self.logger)

    def callback(self, ch, method, properties, body):
        print "---------------------bus consumer-----------------------"
        try:
            data = json.loads(body.decode('utf-8'))
            arr = method.routing_key.split(".")
            routing_suffix = arr[-1]
            if routing_suffix == 'get_station':
                self.get_station_business.get_station(data)
            if routing_suffix == 'gen_feature':
                self.gen_feature.gen_feature(data)
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)


class GetStationBusiness(object):
    """根据线路添加站点"""

    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def get_bus_data(city, line):

        driver.get(dir_path + "/search.html")
        time.sleep(2)
        driver.find_element_by_id('CityName').send_keys(city)
        driver.find_element_by_id('BusLineName').send_keys(line)
        time.sleep(1)
        driver.find_element_by_id('search').click()
        time.sleep(1)
        data1 = driver.find_element_by_id('infobox1').text
        data2 = driver.find_element_by_id('infobox2').text

        return json.loads(data1), json.loads(data2)

    @transaction(is_commit=True)
    def get_station(self, sql_cur, data):
        print "=======================1"
        db = MysqlDbUtil
        route_ids = data['route_ids']
        district_code = data['district_code']
        company_id = data['company_id']

        station_name_sql = "SELECT `number` FROM `bus_station` " \
                           "WHERE `name`='{}' AND `company_id`={} LIMIT 1"
        station_sql = "SELECT `id` FROM `bus_station` " \
                      "WHERE `longitude`={} AND `latitude`={} LIMIT 1"

        busline_sql = "SELECT `id` FROM `bus_route` " \
                      "WHERE `line_no`='{}' and `company_id`={} LIMIT 1"

        relation_sql = "SELECT `id` FROM `route_station_relation` " \
                       "WHERE `code`={} AND `round_trip`={} AND " \
                       "`bus_route_id`={} AND `bus_station_id`={}"

        for lineno in route_ids.split(","):
            go_stations, ret_stations = \
                GetStationBusiness.get_bus_data(district_code, lineno)
            if go_stations and ret_stations:
                group_no = datetime.now().strftime('%Y%m%d%H%M%S%f')

                # 添加线路
                # go_stations round_trip为1
                busline_name = "{}路({}--{})".format(
                    str(lineno), go_stations[0]['name'],
                    go_stations[-1]['name'])
                busline_obj1 = \
                    db.get(sql_cur, busline_sql.format(busline_name, company_id))
                print "busline_obj1={}".format(busline_obj1)
                if not busline_obj1:
                    d = {
                        'line_no': busline_name,
                        'fees': 2,
                        'amount': 2,
                        'status': 1,
                        'round_trip': 1,
                        'start_time': '1937-1-1 07:00:00',
                        'end_time': '1937-1-1 23:00:00',
                        'company_id': company_id,
                        'group_no': group_no
                    }
                    db.insert(sql_cur, d, table_name='bus_route')
                    busline_obj1 = db.get(sql_cur,
                                          busline_sql.format(busline_name, company_id))
                    print "busline_obj1={}".format(busline_obj1)

                # ret_stations round_trip为2
                busline_name = "{}路({}--{})".format(
                    str(lineno), ret_stations[0]['name'],
                    ret_stations[-1]['name'])

                busline_obj2 = db.get(sql_cur, busline_sql.format(busline_name, company_id))
                print "busline_obj2={}".format(str(busline_obj2))
                if not busline_obj2:
                    d = {
                        'line_no': busline_name,
                        'fees': 2,
                        'amount': 2,
                        'status': 1,
                        'round_trip': 2,
                        'start_time': '1937-1-1 07:00:00',
                        'end_time': '1937-1-1 23:00:00',
                        'company_id': company_id,
                        'group_no': group_no
                    }
                    db.insert(sql_cur, d, table_name='bus_route')
                    busline_obj2 = db.get(
                        sql_cur, busline_sql.format(busline_name, company_id))

                # 添加站点
                for station in go_stations:
                    station_name = station['name']
                    gps = station['location']
                    lng = gps['lng']
                    lat = gps['lat']

                    station_obj = db.get(
                        sql_cur, station_sql.format(lng, lat))
                    if not station_obj:
                        station_name_obj = db.get(
                            sql_cur, station_name_sql.format(
                                station_name, company_id))
                        if station_name_obj:
                            patch = station_name_obj[0]
                        else:
                            patch = str(time.time()).replace('.', '')
                        d = {
                            'name': station_name,
                            'status': 1,
                            'longitude': lng,
                            'latitude': lat,
                            'number': patch,
                            'company_id': company_id
                        }
                        db.insert(sql_cur, d, table_name='bus_station')
                        station_obj = db.get(
                            sql_cur, station_sql.format(lng, lat))

                    # 线路站点关系
                    tmp = db.get(sql_cur, relation_sql.format(
                        station['sequence'], 1, busline_obj1[0], station_obj[0]))
                    if not tmp:
                        d = {
                            'code': station['sequence'],
                            'round_trip': 1,
                            'bus_route_id': busline_obj1[0],
                            'bus_station_id': station_obj[0],
                            'company_id': company_id
                        }
                        db.insert(sql_cur, d,
                                  table_name='route_station_relation')

                for station in ret_stations:
                    station_name = station['name']
                    gps = station['location']
                    lng = gps['lng']
                    lat = gps['lat']

                    station_obj = db.get(
                        sql_cur, station_sql.format(lng, lat))
                    if not station_obj:
                        station_name_obj = db.get(
                            sql_cur, station_name_sql.format(station_name, company_id))
                        if station_name_obj:
                            patch = station_name_obj[0]
                        else:
                            patch = str(time.time()).replace('.', '')
                        d = {
                            'name': station_name,
                            'status': 1,
                            'longitude': lng,
                            'latitude': lat,
                            'number': patch,
                            'company_id': company_id
                        }
                        db.insert(sql_cur, d, table_name='bus_station')
                        station_obj = db.get(
                            sql_cur, station_sql.format(lng, lat))

                    # 线路站点关系
                    tmp = db.get(sql_cur, relation_sql.format(
                        station['sequence'], 1, busline_obj2[0],
                        station_obj[0]))
                    if not tmp:
                        d = {
                            'code': station['sequence'],
                            'round_trip': 1,
                            'bus_route_id': busline_obj2[0],
                            'bus_station_id': station_obj[0],
                            'company_id': company_id
                        }
                        db.insert(sql_cur, d,
                                  table_name='route_station_relation')


class GenFeature(object):
    """生成特征值"""
    GET_TOKEN_URL = 'https://aip.baidubce.com/rest/2.0/face/v1/feature'

    def __init__(self, logger):
        self.logger = logger

    @transaction(is_commit=True)
    def gen_feature(self, sql_cur, data):
        db = MysqlDbUtil
        baidu_access_token = rds_conn.get('BAIDU_ACCESS_TOKEN')
        if baidu_access_token:
            fid = data['fid']   # face_img pk
            oss_url = data['oss_url']
            res = requests.get(oss_url)
            image = base64.b64encode(res.content).decode("utf8")
            d = {
                'image': image,
                'image_type': 'BASE64',
                'version': 6002,
                'access_token': baidu_access_token
            }
            res = requests.post(GenFeature.GET_TOKEN_URL, d)
            if res.status_code == 200:
                d = json.loads(res.content)
                if d['error_code'] == 0:
                    result = d['result']
                    if result['face_num'] > 0:
                        feature = result['face_list'][0]['feature']
                        feature_crc = zlib.crc32(feature) & 0xffffffff
                        update_d = {
                            '`id`': fid,
                            '`feature`': feature,
                            '`feature_crc`': feature_crc,
                            '`status`': 3   # 有效
                        }
                        db.update(sql_cur, update_d, table_name='`face_img`')
                    else:
                        update_d = {
                            '`id`': fid,
                            '`status`': 4  # 失败
                        }
                        db.update(sql_cur, update_d, table_name='`face_img`')


class DeviceConsumer(object):
    def __init__(self):
        self.logger = tools.get_logger(config.log_path)
        self.device_business = DeviceBusiness(
            config.Productkey, config.MNSAccessKeyId,
            config.MNSAccessKeySecret, self.logger)

    def device_callback(self, ch, method, properties, body):
        data = json.loads(body.decode('utf-8'))
        arr = method.routing_key.split(".")
        routing_suffix = arr[-1]
        if routing_suffix == 'list':
            self.device_business.device_people_list_upgrade(data)
        if routing_suffix == 'updatechepai':
            self.device_business.update_chepai(data)
        if routing_suffix == 'devwhitelist':
            self.device_business.dev_white_list_msg(data)
        if routing_suffix == 'clearcnt':
            self.device_business.clear_count(data)
        if routing_suffix == 'delallface':
            self.device_business.delete_all_face(data)
        if routing_suffix == 'ossinfo':
            self.device_business.set_oss_info(data)
        # 消息确认
        ch.basic_ack(delivery_tag=method.delivery_tag)


class DeviceBusiness(object):
    """设备业务"""

    tts = "https://wgxing-dev.oss-cn-shanghai." \
          "aliyuncs.com/people/video/qsc.aac"

    def __init__(self, product_key, mns_access_key_id,
                 mns_access_key_secret, logger):
        self.client = AcsClient(mns_access_key_id,
                                mns_access_key_secret, 'cn-shanghai')
        self.product_key = product_key
        self.logger = logger
        self.path = os.path.dirname(__file__) + '/temp'

    def _batch_add_people(self, device_name, url):
        """批量添加人员"""
        jdata = {
            "url": url,
            "cmd": "batchaddface"
        }
        self._pub_msg(device_name, jdata)

    def _publish_del_people_msg(self, device_name, fid):
        """从设备上删除人员"""
        jdata = {
            "cmd": "delface",
            "fid": int(fid)
        }
        self._pub_msg(device_name, jdata)

    def _publish_update_people_msg(self, device_name, fid, nickname,
                                   feature, aac_url):
        """从设备上更新人员"""
        jdata = {
            "cmd": "updateface",
            "fid": int(fid),
            "fno": device_name,
            "name": nickname,
            "feature": feature,
            "ttsurl": aac_url,
            "group": 0,
            "faceurl": "",
            "cardno": ""
        }
        self._pub_msg(device_name, jdata)

    def _publish_add_people_msg(self, device_name, fid, feature, nickname, aac_url):
        """添加人员"""

        jdata = {
            "cmd": "addface",
            "fid": int(fid),
            "fno": device_name,
            "name": nickname,
            "feature": feature,
            "ttsurl": aac_url,
            "group": 0,
            "faceurl": "",
            "go_station": "",
            "return_station": "",
            "school": "",
            "cardno": ""
        }

        self._pub_msg(device_name, jdata)

    def _publish_dev_white_list(self, device_name):
        jdata = {
            "cmd": "devwhitelist",
            "pkt_inx": -1
        }
        self._pub_msg(device_name, jdata)

    def _pub_msg(self, devname, jdata):
        print u"-----------加入顺序发送消息的队列--------"
        k = rds_conn.get("stream_no_incr")
        if k:
            stream_no = rds_conn.incr("stream_no_incr")
        else:
            rds_conn.set("stream_no_incr", 1000000)
            stream_no = 1000000
        jdata["stream_no"] = stream_no
        k = "mns_list_" + devname
        rds_conn.rpush(k, json.dumps(jdata, encoding="utf-8"))

    def _set_workmode(self, device_name, workmode, chepai, cur_volume, person_limit):
        """
        设置设备工作模式 0车载 1通道闸口 3注册模式
        :param device_name:
        :param workmode:
        :return:
        """
        if workmode not in [0, 1, 3]:
            return -1
        if not cur_volume:
            cur_volume = 100
        cur_volume = cur_volume - 94
        if not chepai:
            return
        jdata = {
            "cmd": "syntime",
            "time": int(time.time()),
            "chepai": chepai.encode('utf-8'),
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
            'person_limit': person_limit
        }

        return self._pub_msg(device_name, jdata)

    def dev_white_list_msg(self, data):
        dev_name = data['dev_name']
        self._publish_dev_white_list(dev_name)

    def update_chepai(self, data):
        chepai = data['chepai']
        device_name = data['device_name']
        cur_volume = data['cur_volume']
        workmode = data['workmode']
        person_limit = data['person_limit']
        self._set_workmode(device_name, int(workmode), chepai, cur_volume, person_limit)

    @transaction(is_commit=False)
    def device_people_list_upgrade(self, pgsql_cur, data):
        """设备人员更新"""
        pgsql_db = MysqlDbUtil
        print(">>>>> device_people_list_upgrade")
        self.logger.error("device_people_list_upgrade")
        add_list = data['add_list']         # fid
        del_list = data['del_list']         # fid
        update_list = data['update_list']   # fid
        device_name = data['device_name']

        # del list
        if len(del_list) < 60:
            print 'del_list', del_list
            for fid in del_list:
                self._publish_del_people_msg(device_name, fid)

        feature_sql = "SELECT feature FROM face_img WHERE id = {}"
        # update list
        if len(update_list) < 60:
            for fid in update_list:
                obj = pgsql_db.get(
                    pgsql_cur, feature_sql.format(fid))
                print obj
                if obj:
                    print obj
                    self._publish_update_people_msg(
                        device_name, fid, "", obj[0], "")

        # add list
        if len(add_list) < 60:
            for fid in add_list:
                obj = pgsql_db.get(
                    pgsql_cur, feature_sql.format(fid))
                if obj:
                    print obj
                    self._publish_add_people_msg(
                        device_name, fid, obj[0], "", "")

    def clear_count(self, data):
        """清空车内人数"""
        device_name = data['device_name']
        jdata = {
            "cmd": "clearcnt",
            "value": 0
        }
        self._pub_msg(device_name, jdata)

    def delete_all_face(self, data):
        """清空车内人数"""
        device_name = data['device_name']
        jdata = {
            "cmd": "delallface"
        }
        self._pub_msg(device_name, jdata)

    def set_oss_info(self, data):
        """设置oss信息"""
        device_name = data['device_name']
        jdata = {
            "cmd": "ossinfo",
            "ossdomain": config.OSSDomain,
            "osskeyid": config.OSSAccessKeyId,
            "osskeysecret": config.OSSAccessKeySecret[12:] + config.OSSAccessKeySecret[:12]
        }
        self._pub_msg(device_name, jdata)

