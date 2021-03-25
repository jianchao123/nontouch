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

    OSSDomain = 'https://wgxing-dev.oss-cn-beijing.aliyuncs.com'
    OSSAccessKeyId = 'LTAIWE5CGeOiozf7'
    OSSAccessKeySecret = 'IGuoRIxwMlPQqJ9ujWyTvSq2em4RDj'
    OSSEndpoint = 'oss-cn-beijing.aliyuncs.com'
    OSSBucketName = 'wgxing-dev'

    # 公交项目使用redis db3
    RedisDb = 3
else:

    mysql_host = '127.0.0.1'
    mysql_passwd = "kIhHAWexFy7pU8qM"

    log_path = "/data/logs/{}/msgqueue".format(project_name)
    mysql_user = "root"

    OSSDomain = 'https://wgxing-pro.oss-cn-zhangjiakou.aliyuncs.com'
    OSSAccessKeyId = 'LTAIWE5CGeOiozf7'
    OSSAccessKeySecret = 'IGuoRIxwMlPQqJ9ujWyTvSq2em4RDj'
    OSSEndpoint = 'oss-cn-zhangjiakou.aliyuncs.com'
    OSSBucketName = 'wgxing-pro'
    RedisDb = 3

redis_conf = dict(host="127.0.0.1", port=6379, db=RedisDb, decode_responses=True)
mysql_conf = dict(host=mysql_host, db="wuganxing_1", port=3306, user=mysql_user,
                  passwd=mysql_passwd, charset="utf8")

logger = get_logger(log_path)
logger.info('--------NONTOUCH_1={}---------------'.format(env))
print env