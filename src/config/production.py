# coding:utf-8

from .default import Config


class ProductionConfig(Config):
    """
    产品环境配置数据
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = \
        'mysql://root:kIhHAWexFy7pU8qM@test.wgxing.com/wuganxing_1'
    LOG_PATH = '/data/logs/nontouch_1/main'

    WGX_CLIENT_CONFIG = dict(
        Productkey='a1agDqZJSpQ',
        ProductHost='a1agDqZJSpQ.iot-as-mqtt.cn-shanghai.aliyuncs.com',
        ProductSecret='SRXmMyDqCb9iIzez',
        DeviceSecret='4c1f6d157b5f518585bb363acbec0071',

        OSSDomain='https://pangang-nontouch_1.oss-cn-beijing.aliyuncs.com',
        OSSAccessKeyId='LTAI4GKiKL9WaoezWEPy8xE6',
        OSSAccessKeySecret='GfuAptYtx2wIbX0vy7xAdmRoGOwo7r',
        OSSEndpoint='http://oss-cn-beijing.aliyuncs.com',
        OSSBucketName='pangang-nontouch_1',
        MNSEndpoint='http://1083695407857925.mns.cn-shanghai.aliyuncs.com/',
        MNSAccessKeyId='LTAI4GHswktoXpmVTnYnkEnf',
        MNSAccessKeySecret='oW4jtV1FEJzcb8BnSFhhlIpSjL0E6G'
    )
