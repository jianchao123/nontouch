# coding: utf-8
import json
import time
import urllib
import requests
from msgqueue import conf
from msgqueue import utils
from msgqueue.db import transaction, MysqlDbUtil


class HeartBeatConsumer(object):

    def __init__(self):
        self.logger = utils.get_logger(conf.log_path)

    def heartbeat_callback(self, ch, method, properties, body):
        print "------------heartbeat-------------deliver_tag={}".\
            format(method.delivery_tag)
        # 消息确认
        ch.basic_ack(delivery_tag=method.delivery_tag)


class BusConsumer(object):

    def __init__(self):
        self.logger = utils.get_logger(conf.log_path)
        self.get_station_business = GetStationBusiness(self.logger)

    def callback(self, ch, method, properties, body):
        print method
        data = json.loads(body.decode('utf-8'))
        arr = method.routing_key.split(".")
        routing_suffix = arr[-1]
        if routing_suffix == 'get_station':
            self.get_station_business.get_station(data)
        # 消息确认
        ch.basic_ack(delivery_tag=method.delivery_tag)


class GetStationBusiness(object):

    def __init__(self, logger):
        self.logger = logger

    @transaction(is_commit=True)
    def get_station(self, sql_cur, data):
        print "============================="
        db = MysqlDbUtil
        route_ids = data['route_ids']
        district_code = data['district_code']
        company_id = data['company_id']

        station_name_sql = "SELECT `number` FROM `bus_station` " \
                           "WHERE `name`='{}' AND `company_id`={} LIMIT 1"
        station_sql = "SELECT `id` FROM `bus_station` " \
                      "WHERE `longitude`={} AND `latitude`={} LIMIT 1"

        busline_sql = "SELECT `id` FROM `bus_route` " \
                      "WHERE `line_no`='{}' LIMIT 1"
        req_url = "https://ditu.amap.com/service/poiBus?" \
                  "query_type=TQUERY&pagesize=20&pagenum=1&qii=true&cluster_state=5&" \
                  "need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&" \
                  "is_classify=true&zoom=9.72&" \
                  "city={}&src=mypage&callnative=0&innersrc=uriapi&keywords={}"
        relation_sql = "SELECT `id` FROM `route_station_relation` " \
                       "WHERE `code`={} AND `round_trip`={} AND " \
                       "`bus_route_id`={} AND `bus_station_id`={}"

        for lineno in route_ids.split(","):
            key_name = str(lineno) + "路"
            url = req_url. \
                format(district_code, urllib.quote(key_name.encode('utf8')))
            res = requests.get(url)
            d = json.loads(res.content)
            print d
            buslines = []
            if int(d['status']) == 1:
                more_data = d['busMoreData']
                if int(more_data['total']) > 1:
                    busline_list = more_data['busline_list']
                    for row in busline_list:
                        if row['key_name'] == key_name:
                            buslines.append(row['via_stops'])
            if buslines:
                go_stations = buslines[0]
                ret_stations = buslines[1]

                # 添加线路
                # go_stations round_trip为1
                busline_name = "{}路({}--{})".format(
                    str(lineno), go_stations[0]['name'],
                    go_stations[-1]['name'])

                busline_obj1 = db.get(sql_cur, busline_sql.format(busline_name))
                if not busline_obj1:
                    d = {
                        'line_no': busline_name,
                        'fees': 2,
                        'amount': 2,
                        'status': 1,
                        'round_trip': 1,
                        'start_time': '1937-1-1 07:00:00',
                        'end_time': '1937-1-1 23:00:00',
                        'company_id': company_id
                    }
                    db.insert(sql_cur, d, table_name='bus_route')
                    busline_obj1 = db.get(sql_cur,
                                          busline_sql.format(busline_name))

                # ret_stations round_trip为2
                busline_name = "{}路({}--{})".format(
                    str(lineno), ret_stations[0]['name'],
                    ret_stations[-1]['name'])

                busline_obj2 = db.get(sql_cur, busline_sql.format(busline_name))
                if not busline_obj2:
                    d = {
                        'line_no': busline_name,
                        'fees': 2,
                        'amount': 2,
                        'status': 1,
                        'round_trip': 2,
                        'start_time': '1937-1-1 07:00:00',
                        'end_time': '1937-1-1 23:00:00',
                        'company_id': company_id
                    }
                    db.insert(sql_cur, d, table_name='bus_route')
                    busline_obj2 = db.get(
                        sql_cur, busline_sql.format(busline_name))

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
