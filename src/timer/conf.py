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

    redis_conf = dict(host="127.0.0.1", port=6379, db=0)

    mysql_conf = dict(host="127.0.0.1", port=3306, db="wuganxing_1",
                      user="root", passwd="kIhHAWexFy7pU8qM", charset="utf8")

    OSSDomain = 'https://wgxing-test.oss-cn-zhangjiakou.aliyuncs.com'
    OSSAccessKeyId = 'LTAIWE5CGeOiozf7'
    OSSAccessKeySecret = 'IGuoRIxwMlPQqJ9ujWyTvSq2em4RDj'
    OSSEndpoint = 'oss-cn-zhangjiakou.aliyuncs.com'
    OSSBucketName = 'wgxing-test'

elif env == "DEV":
    log_path = project_dir + "/logs/timer"
    print log_path
    url = ""

    # 公交项目使用redis db3
    redis_conf = dict(host="127.0.0.1", port=6379, db=3, decode_responses=True)

    mysql_conf = dict(host="127.0.0.1", port=3306, db="wuganxing_1",
                      user="root", passwd="kIhHAWexFy7pU8qM", charset="utf8")

    OSSDomain = 'https://wgxing-dev.oss-cn-beijing.aliyuncs.com'
    OSSAccessKeyId = 'LTAIWE5CGeOiozf7'
    OSSAccessKeySecret = 'IGuoRIxwMlPQqJ9ujWyTvSq2em4RDj'
    OSSEndpoint = 'oss-cn-beijing.aliyuncs.com'
    OSSBucketName = 'wgxing-dev'


else:

    log_path = "/data/logs/{}/timer".format(project_name)
    url = ""

    redis_conf = dict(host="127.0.0.1", port=6379, db=0, decode_responses=True)

    mysql_conf = dict(host="127.0.0.1", port=3306, db="wuganxing_1",
                      user="root", passwd="kIhHAWexFy7pU8qM", charset="utf8")

    OSSDomain = 'https://wgxing-pro.oss-cn-zhangjiakou.aliyuncs.com'
    OSSAccessKeyId = 'LTAIWE5CGeOiozf7'
    OSSAccessKeySecret = 'IGuoRIxwMlPQqJ9ujWyTvSq2em4RDj'
    OSSEndpoint = 'oss-cn-zhangjiakou.aliyuncs.com'
    OSSBucketName = 'wgxing-pro'


logger = get_logger(log_path)
logger.info('--------NONTOUCH_1={}---------------'.format(env))
print env
