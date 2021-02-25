# coding: utf-8
"""
订阅者
"""
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
import time
import threading

current_dir = os.path.dirname(os.path.realpath(__file__))
current_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)

import pika
from msgqueue.consume_business import BusConsumer
from msgqueue.consume_business import HeartBeatConsumer

print("start subscriber")


def start_subscriber():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', heartbeat=0))
    channel = connection.channel()
    # 声明交换机
    # Exchange为topic时,生产者可以指定一个支持通配符的RoutingKey（如demo.*）
    # 发向此Exchange,凡是Exchange上RoutingKey满足此通配符的Queue就会收到消息
    channel.exchange_declare(exchange='bus_exchange', exchange_type='topic')
    channel.exchange_declare(exchange='heartbeat_exchange',
                             exchange_type='topic')

    # 声明消息队列, durable消息队列持久化
    channel.queue_declare(queue="bus_queue", durable=False)
    channel.queue_declare(queue='heartbeat_queue', durable=False)

    # 绑定交换机和队列(一个交换机可以绑定多个队列)
    # routing_key路由器(绑定到队列上),携带该路由的消息都将被分发到该消息队列
    channel.queue_bind(exchange='bus_exchange',
                       queue="bus_queue",
                       routing_key="bus.*")
    channel.queue_bind(exchange='heartbeat_exchange',
                       queue="heartbeat_queue",
                       routing_key="heartbeat")

    channel.basic_qos(prefetch_count=1)

    # 消费者 auto_ack=False设置为手动确认消息
    bus_consumer = BusConsumer()
    channel.basic_consume(
        queue="bus_queue",
        on_message_callback=bus_consumer.callback,
        auto_ack=False)

    heartbeat_consumer = HeartBeatConsumer()
    channel.basic_consume(
        queue="heartbeat_queue",
        on_message_callback=heartbeat_consumer.heartbeat_callback,
        auto_ack=False
    )

    channel.start_consuming()


# no_ack=False
# 只要consumer手动应答了Basic.Ack,就算其"成功"处理了

# prefetch_count
# 由于消费者自身处理能力有限,从rabbitmq获取一定数量的消息后,
# 希望rabbitmq不再将队列中的消息推送过来,当对消息处理完后
# (即对消息进行了ack,并且有能力处理更多的消息)再接收来自队列的消息.
# 在这种场景下,我们可以通过设置basic.qos信令中的prefetch_count来达到这种效果


# 订阅者启动
if __name__ == "__main__":
    start_subscriber()
