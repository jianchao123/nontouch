# coding: utf-8
import os
from utils import get_logger

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
    user = "root"

elif env == "DEV":
    mysql_host = '127.0.0.1'
    mysql_passwd = "kIhHAWexFy7pU8qM"

    log_path = project_dir + "/logs/msgqueue"
    user = "root"

    Productkey = 'a1vperyb2Cg'
    ProductHost = 'a1vperyb2Cg.iot-as-mqtt.cn-shanghai.aliyuncs.com'
    ProductSecret = 'jqSbrJZ11baH1aAH'
    DeviceSecret = 'bmq66tsx0OGju0CGqeYjzCTYlwA454j0'  # 'CVAp97tAUayElJwRbiXAiTgcoCZZAX1j'

    OSSDomain = 'https://wgxing-device.oss-cn-beijing.aliyuncs.com'
    OSSAccessKeyId = 'LTAIWE5CGeOiozf7'
    OSSAccessKeySecret = 'IGuoRIxwMlPQqJ9ujWyTvSq2em4RDj'
    OSSEndpoint = 'http://oss-cn-beijing.aliyuncs.com'
    OSSBucketName = 'wgxing-device'

    MNSEndpoint = 'http://1162097573951650.mns.cn-shanghai.aliyuncs.com/'
    MNSAccessKeyId = 'LTAI4GL6gtEc4bnmj82yQ9wc'
    MNSAccessKeySecret = 'vhuBLJpqlOsSisnuUQ1xvE02GCXhIC'
else:

    mysql_host = '127.0.0.1'
    mysql_passwd = "kIhHAWexFy7pU8qM"

    log_path = "/data/logs/{}/msgqueue".format(project_name)
    user = "root"

    Productkey = 'a1agDqZJSpQ'
    ProductHost = 'a1agDqZJSpQ.iot-as-mqtt.cn-shanghai.aliyuncs.com'
    ProductSecret = 'SRXmMyDqCb9iIzez'
    DeviceSecret = '4c1f6d157b5f518585bb363acbec0071'  # 'CVAp97tAUayElJwRbiXAiTgcoCZZAX1j'

    OSSDomain = 'https://pangang-nontouch_1.oss-cn-beijing.aliyuncs.com'
    OSSAccessKeyId = 'LTAI4GKiKL9WaoezWEPy8xE6'
    OSSAccessKeySecret = 'GfuAptYtx2wIbX0vy7xAdmRoGOwo7r'
    OSSEndpoint = 'http://oss-cn-beijing.aliyuncs.com'
    OSSBucketName = 'pangang-nontouch_1'

    MNSEndpoint = 'http://1083695407857925.mns.cn-shanghai.aliyuncs.com/'
    MNSAccessKeyId = 'LTAI4GHswktoXpmVTnYnkEnf'
    MNSAccessKeySecret = 'oW4jtV1FEJzcb8BnSFhhlIpSjL0E6G'


redis_conf = dict(host="127.0.0.1", port=6379, db=0, decode_responses=True)
mysql_conf = dict(host=mysql_host, db="nontouch_1", port=3306, user=user,
                  passwd=mysql_passwd, charset="utf8")

logger = get_logger(log_path)
logger.info('--------NONTOUCH_1={}---------------'.format(env))
print env