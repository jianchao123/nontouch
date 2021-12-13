# coding:utf-8
import os
from tools import get_logger
project_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(project_dir)
project_dir = os.path.dirname(project_dir)

project_name = "nontouch_1"
env_dist = os.environ
env = env_dist.get('NONTOUCH_1_ENV')


if env == 'PRO':

    log_path = "/data/logs/{}/timer".format(project_name)
    url = ""

    redis_conf = dict(host="127.0.0.1", port=6379, db=0, decode_responses=True)

    mysql_conf = dict(host="127.0.0.1", port=3306, db="wuganxing_1",
                      user="root", passwd="kIhHAWexFy7pU8qM", charset="utf8")

    OSSDomain = 'https://wgxing-pro.oss-cn-zhangjiakou.aliyuncs.com'
    OSSAccessKeyId = 'LTAI5tHYr3CZ59HCRLEocbDG'
    OSSAccessKeySecret = 'BMRI8WzUVMRbS6LHPM3bIiadWIPE8c'
    OSSEndpoint = 'oss-cn-zhangjiakou.aliyuncs.com'
    OSSBucketName = 'wgxing-pro'

    BAIDU_APP_ID = '24831550'
    BAIDU_API_KEY = 'GXxpMgNvAaQxzXfXVe0q7fvZ'
    BAIDU_SECRET_KEY = 'Xg0eChKitGhYSEeEudVtKpD41iuSCkgB'

elif env == "TEST":
    log_path = "/data/logs/{}/timer".format(project_name)
    url = ""

    redis_conf = dict(host="127.0.0.1", port=6379, db=0)

    mysql_conf = dict(host="127.0.0.1", port=3306, db="wuganxing_1",
                      user="root", passwd="kIhHAWexFy7pU8qM", charset="utf8")

    OSSDomain = 'https://wgxing-test.oss-cn-zhangjiakou.aliyuncs.com'
    OSSAccessKeyId = 'LTAI5tHYr3CZ59HCRLEocbDG'
    OSSAccessKeySecret = 'BMRI8WzUVMRbS6LHPM3bIiadWIPE8c'
    OSSEndpoint = 'oss-cn-zhangjiakou.aliyuncs.com'
    OSSBucketName = 'wgxing-test'

    BAIDU_APP_ID = '24831552'
    BAIDU_API_KEY = 'ZKkHrawGz9v8lSB9GB8SBHxR'
    BAIDU_SECRET_KEY = 'yfHHmzhRzapTVd9uczLxTLCH33IOAb5x'

else:
    log_path = project_dir + "/logs/timer"
    print log_path
    url = ""

    # 公交项目使用redis db3
    redis_conf = dict(host="127.0.0.1", port=6379, db=3, decode_responses=True)

    mysql_conf = dict(host="127.0.0.1", port=3306, db="wuganxing_1",
                      user="root", passwd="kIhHAWexFy7pU8qM", charset="utf8")

    OSSDomain = 'https://wgxing-dev.oss-cn-beijing.aliyuncs.com'
    OSSAccessKeyId = 'LTAI5tHYr3CZ59HCRLEocbDG'
    OSSAccessKeySecret = 'BMRI8WzUVMRbS6LHPM3bIiadWIPE8c'
    OSSEndpoint = 'oss-cn-beijing.aliyuncs.com'
    OSSBucketName = 'wgxing-dev'

    BAIDU_APP_ID = '24831558'
    BAIDU_API_KEY = 'Si8bUb5dIqK4ZwtiKL5tFkKP'
    BAIDU_SECRET_KEY = 'XNRNi6MpIZjBqfSN0adcOHIPOk2GQVEk'


logger = get_logger(log_path)
logger.info('--------NONTOUCH_1={}---------------'.format(env))
print env
