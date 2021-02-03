# coding:utf8
import json
import requests
import urllib

key_name = u'131路'
district_code = 510100
url = "https://ditu.amap.com/service/poiBus?" \
      "query_type=TQUERY&pagesize=20&pagenum=1&qii=true&cluster_state=5&" \
      "need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&" \
      "is_classify=true&zoom=9.72&" \
      "city={}&src=mypage&callnative=0&innersrc=uriapi&keywords={}".\
    format(district_code, urllib.quote(key_name.encode('utf8')))
res = requests.get(url)
d = json.loads(res.content)
buslines = []
if int(d['status']) == 1:
    more_data = d['busMoreData']
    if int(more_data['total']) > 1:
        busline_list = more_data['busline_list']
        for row in busline_list:
            if row['key_name'] == key_name:
                buslines.append(row)
go_stations = buslines[0]
ret_stations = buslines[1]
print go_stations
print ret_stations
