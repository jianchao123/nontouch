# coding:utf-8
import os
from t_logging import get_logger
project_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(project_dir)
project_dir = os.path.dirname(project_dir)

project_name = "nontouch_1"
env_dist = os.environ
env = env_dist.get('NONTOUCH_1_ENV')

if env == "TEST":
    log_path = "/data/logs/{}/timer".format(project_name)
    url = ""

    redis_conf = dict(host="127.0.0.1", port=6379, db=0,
                      password="kIhHAWexFy7pU8qM", decode_responses=True)

    mysql_conf = dict(host="127.0.0.1", port=3306, db="nontouch_1",
                      user="root", passwd="kIhHAWexFy7pU8qM", charset="utf8")

elif env == "DEV":
    log_path = project_dir + "/logs/timer"
    print log_path
    url = ""

    redis_conf = dict(host="127.0.0.1", port=6379, db=0, decode_responses=True)

    mysql_conf = dict(host="127.0.0.1", port=3306, db="wuganxing_1",
                      user="root", passwd="kIhHAWexFy7pU8qM", charset="utf8")

    OSSDomain = 'https://.oss-cn-beijing.aliyuncs.com'
    OSSAccessKeyId = 'LTAIWE5CGeOiozf7'
    OSSAccessKeySecret = 'IGuoRIxwMlPQqJ9ujWyTvSq2em4RDj'
    OSSEndpoint = 'oss-cn-beijing.aliyuncs.com'
    OSSBucketName = 'wgxing-dev'


else:

    log_path = "/data/logs/{}/timer".format(project_name)
    url = ""

    redis_conf = dict(host="127.0.0.1", port=6379, db=0, decode_responses=True)

    mysql_conf = dict(host="127.0.0.1", port=3306, db="nontouch_1",
                      user="root", passwd="kIhHAWexFy7pU8qM", charset="utf8")

    Productkey = 'a1agDqZJSpQ'
    ProductHost = 'a1agDqZJSpQ.iot-as-mqtt.cn-shanghai.aliyuncs.com'
    ProductSecret = 'SRXmMyDqCb9iIzez'
    DeviceSecret = '4c1f6d157b5f518585bb363acbec0071'  # 'CVAp97tAUayElJwRbiXAiTgcoCZZAX1j'

    OSSDomain = 'https://.oss-cn-beijing.aliyuncs.com'
    OSSAccessKeyId = ''
    OSSAccessKeySecret = ''
    OSSEndpoint = 'http://oss-cn-beijing.aliyuncs.com'
    OSSBucketName = ''


logger = get_logger(log_path)
logger.info('--------NONTOUCH_1={}---------------'.format(env))
print env
