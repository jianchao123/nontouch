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


# 测试用户创建
if __name__ == "__main__":
    # generate_create_user_msg(12)
    generate_get_station_msg('201,202,203,209,5,6,7,8', 511302, 8)
