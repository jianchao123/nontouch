# coding: utf-8
import os
from tools import get_logger

project_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(project_dir)
project_dir = os.path.dirname(project_dir)
env_dist = os.environ
env = env_dist.get('NONTOUCH_1_ENV')

project_name = "nontouch_1"

if env == "TEST":
    mysql_host = '127.0.0.1'
    mysql_passwd = "kIhHAWexFy7pU8qM"

    log_path = "/data/logs/{}/msgqueue".format(project_name)
    mysql_user = "root"
    RedisDb = 3

elif env == "DEV":
    mysql_host = '127.0.0.1'
    mysql_passwd = "kIhHAWexFy7pU8qM"

    log_path = project_dir + "/logs/msgqueue"
    mysql_user = "root"

    # 物联网
    Productkey = 'a16h4zdWCqM'
    ProductHost = 'a16h4zdWCqM.iot-as-mqtt.cn-shanghai.aliyuncs.com'
    ProductSecret = 'VYMQSqHamIQgREVi'
    DeviceSecret = '7e4984b8f75aaa60872e3bb8ee8b58f4'

    OSSDomain = 'https://wgxing-dev.oss-cn-beijing.aliyuncs.com'
    OSSAccessKeyId = 'LTAI5tHYr3CZ59HCRLEocbDG'
    OSSAccessKeySecret = 'BMRI8WzUVMRbS6LHPM3bIiadWIPE8c'
    OSSEndpoint = 'oss-cn-beijing.aliyuncs.com'
    OSSBucketName = 'wgxing-dev'

    MNSEndpoint = 'http://1162097573951650.mns.cn-shanghai.aliyuncs.com'
    MNSAccessKeyId = 'LTAI5tLzBs74j8dEX4A8TPy6'
    MNSAccessKeySecret = 'uLU5qLEdxet7IZ6w7uB3t7U5PVo15F'

    # 公交项目使用redis db3
    RedisDb = 3
else:

    mysql_host = '127.0.0.1'
    mysql_passwd = "kIhHAWexFy7pU8qM"

    log_path = "/data/logs/{}/msgqueue".format(project_name)
    mysql_user = "root"

    # 物联网
    Productkey = 'a16h4zdWCqM'
    ProductHost = 'a16h4zdWCqM.iot-as-mqtt.cn-shanghai.aliyuncs.com'
    ProductSecret = 'VYMQSqHamIQgREVi'
    DeviceSecret = '7e4984b8f75aaa60872e3bb8ee8b58f4'

    OSSDomain = 'https://wgxing-pro.oss-cn-zhangjiakou.aliyuncs.com'
    OSSAccessKeyId = 'LTAI5tHYr3CZ59HCRLEocbDG'
    OSSAccessKeySecret = 'BMRI8WzUVMRbS6LHPM3bIiadWIPE8c'
    OSSEndpoint = 'oss-cn-zhangjiakou.aliyuncs.com'
    OSSBucketName = 'wgxing-pro'

    MNSEndpoint = 'http://1162097573951650.mns.cn-shanghai-internal.aliyuncs.com'
    MNSAccessKeyId = 'LTAI5tLzBs74j8dEX4A8TPy6'
    MNSAccessKeySecret = 'uLU5qLEdxet7IZ6w7uB3t7U5PVo15F'

    RedisDb = 3

redis_conf = dict(host="127.0.0.1", port=6379, db=RedisDb, decode_responses=True)
mysql_conf = dict(host=mysql_host, db="wuganxing_1", port=3306, user=mysql_user,
                  passwd=mysql_passwd, charset="utf8")

logger = get_logger(log_path)
logger.info('--------NONTOUCH_1={}---------------'.format(env))
print env