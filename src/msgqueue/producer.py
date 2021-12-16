# coding:utf-8
"""
所有消息的定义在此文件定义
业务层调用 generate_create_company_msg  generate_create_user_msg
"""
import json
import pika

queue_conn = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost', heartbeat=0))
channel = queue_conn.channel()
# channel.exchange_declare(exchange='user_exchange', exchange_type='topic')
# channel.exchange_declare(exchange='device_exchange', exchange_type='topic')
# channel.exchange_declare(exchange='excel_exchange', exchange_type='topic')
channel.exchange_declare(exchange='bus_exchange', exchange_type='topic')
channel.exchange_declare(exchange='device_exchange', exchange_type='topic')


def _publish_msg(exchange, routing_key, message):
    """发布消息"""
    channel.basic_publish(exchange=exchange,
                          routing_key=routing_key,
                          body=message, mandatory=True)


def generate_get_station_msg(route_ids, district_code, company_id):
    """获取线路站点"""
    data = {
        'route_ids': route_ids,
        'district_code': district_code,
        'company_id': company_id,
    }
    _publish_msg('bus_exchange', 'bus.get_station', json.dumps(data))


def heartbeat():
    """msg心跳"""
    _publish_msg('heartbeat_exchange', 'heartbeat',
                 json.dumps({'heartbeat': 1}))


def gen_feature(fid, oss_url):
    """生成feature"""
    data = {
        'fid': fid,
        'oss_url': oss_url
    }
    _publish_msg('bus_exchange', 'bus.gen_feature', json.dumps(data))


# 设备相关
def delete_all_face(device_name):
    data = {'device_name': device_name}
    _publish_msg('device_exchange', 'device.delallface', json.dumps(data))


def update_chepai(device_name, chepai, cur_volume, workmode, person_limit):
    """更新车牌"""
    data = {
        "chepai": chepai,
        "device_name": device_name,
        "cur_volume": cur_volume,
        "workmode": workmode,
        "person_limit": person_limit
    }
    _publish_msg('device_exchange', 'device.updatechepai', json.dumps(data))


def dev_while_list(device_name):
    data = {
        'dev_name': device_name
    }
    _publish_msg('device_exchange', 'device.devwhitelist', json.dumps(data))


def device_person_update_msg(add_list, del_list, update_list, device_name):
    """设备人员列表更新"""
    data = {
        "add_list": add_list,
        "del_list": del_list,
        "update_list": update_list,
        "device_name": device_name
    }
    _publish_msg('device_exchange', 'device.list', json.dumps(data))


def device_oss_info(device_name):
    """oss 信息"""
    data = {
        "device_name": device_name
    }
    _publish_msg('device_exchange', 'device.ossinfo', json.dumps(data))

# 测试用户创建
if __name__ == "__main__":
    # generate_create_user_msg(12)
    generate_get_station_msg('蓬安201路,蓬安202路,蓬安203路,蓬安209路,蓬安5路,蓬安6路,蓬安7路,蓬安8路', "南充", 9)
