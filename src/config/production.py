# coding:utf-8

from .default import Config


class ProductionConfig(Config):
    """
    产品环境配置数据
    """
    # Flask config
    DEBUG = False
    TESTING = True

    # Redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = ''

    # Mysql
    SQLALCHEMY_DATABASE_URI = \
        'mysql://root:kIhHAWexFy7pU8qM@127.0.0.1/wuganxing_1'

    LOG_PATH = '/data/logs/nontouch_1/main'

    # 阿里云OSS
    OSS_BUCKET = "wgxing-pro"
    OSS_REGION = "oss-cn-zhangjiakou"
    OSS_POINT = "oss-cn-zhangjiakou.aliyuncs.com"
    OSS_ALL_KEY = "LTAIWE5CGeOiozf7"  # 所有权限
    OSS_ALL_SECRET = "IGuoRIxwMlPQqJ9ujWyTvSq2em4RDj"

    PAY_HOST = 'https://wgxing.com'

    # 支付宝支付
    APP_ID = '2019121169830445'
    RechargeUrl = '/callback/ali-recharge/'
    NOTIFY_URL = PAY_HOST + RechargeUrl
    ALIPAY_GATEWAY = 'https://openapi.alipay.com/gateway.do'
    APP_PRIVATE_KEY = 'MIIEogIBAAKCAQEAoeQqNeZVf40SSJKNBLDF7KMNV8H5jPRoZ8Nbps2jtGT/6iCT9n9Qzs4ihHkCZeDMeW6Peh4otCDHCNV1a9K3WGsGP12INyd8V2VQ7QJ59TsaEnbQvFWHPyTWtU9rsMIfpyqwiO7gMS7LBMGNBVjrdGyJroMierS4nue7vQokFLAEbgkQW5WLRXBppdhlhygAdbx43aSyG67P3Zs/ptqZ+q7wbwhThFstE4V0VG39z7KHnKhle64+AwEvjEEEux7UekFZxyjjTn0VYP+yFxTdmMXvgEhiBWAEje5xTHhiO8iNxN0f7amUk5HTZhJhBQL+9VJhmBd6n+w1ea9rofBHPwIDAQABAoIBABxNJ/fuQWof/l9Dh3WXdbJtuspptbenjoz9QQuDDahes8J5WYSRM05ECRLBmOK4juZ3pouBtDnxNPpdXr6vwq+pXhk7v7FsrLcWljQo56swXtl1ff4+sXsfdI2Tyc7H0QLHWr9Fi1ntxT4anA2gQuFCjDs+34s2BsR43IAqwq3+5DOMYmZLPZCPHFxKyLQ36xAlOUs+pqzngcXpAdRJJbmQ9RBp+/3kO+2j3jvFawOyjPClQKWlE24fyZNPbdgJ2B151C846MxemSQP7r9Gtm0Tiob8aTUwJA+xELTBfXRjF5s54WOS8HfsBoELyuDg2NaECBW3IYcAUO5LTxtVgkkCgYEA1dH3MuLuhmjIrpSyKYruR+pYLi6s24FHLJOD28kqC0DJII0/UYNTGlk6a3waayfLXR8uJcubIGj6BGhnTRAqBdbtuwboYmJQcA96kU1Om/mOFODoYNUnADJTd8f6+e/8ZQeX2Gw4mqHqm3GqCT6rrfOF3k5iofK96i5VgC2yCcUCgYEAwdPC5q80A/NGZnZG5uXM1Ipm9pdIxYUEZCKAgQqOy3yuXIgjZ37CLxAwiXH5dm6qk3W4P30uJpRkcNo5ulxsMKIqfdveGSvTJR0e6BiBglvC2FqfZDSYLSPgJORdiiDW3L0l5N4BxGjqqrbMIn2duuOdTtnpmJyxtAJNTvvtUTMCgYA1KfKj1WbnRpB3UAOIbsHWYb8xJGvYXCl9PORxNnBcwewASv5uXw+/omXzKbVL5WYcLk+EGD7m7RMVG3xr3dQFBa6wbQREyhsj8cVQ8X7VK1SXfmBpCzaaRukYBEIz+OaxnBS2PBpK4G173uQfTlTTeJRVdPnzOG7eFk0uBK6a3QKBgEtN8K0baMQYIkPws/9FTN1OoE4x3K4QzfHxjaeU6IGagUumAMtW7i7GxXTA+UDQIimEVP8lrWaDxLorrr3+5nHGr2eSoql442HJ/JYD3108NWlFXCPcYzs2cwEiUE04EQJV4oEW1+ztLi8BMjI8R6mygQ1/kEggqNHdCxgivMMNAoGAfZyo5mnwiCOWshlg4/vYmQQuhVP+b8ZQDxZkj84Q5/ARqsZ5WIzcpZWU4xaviBO6hUaxyDv/evd00CanUCKF7t8XrHkMI6MsqsbRhCuDBSq34878k+svK1GgDoZUdnVH/zkNw/eKReAbmGgmCEEOSnHXEAak7dce/nyPjKR/PFo='
    ALIPAY_PUBLIC_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnUyTSsCGBC+rhqAoGwOXNTRvafK7qRChmJKNLhersqyck+99Mb1xal+iqUEy9qCpDntWa/qB5XHUclRz2MrP//66CJKWAAaU+6zOKTekBuEd83eDedY5nlrBrBcvs2d841dRIvePksEhI9CGt26/d9LlN8o97vrjgiNdKytPOGKdCNF0e998XFWVD1sxvkyFW6ySy2j3BKyL1DVG4brU5KE6jgp782XOIgvPXKn6N2DR/5D69QMijZAQ0UCVsPspVDdC6MfbmjSRJEPP7qsrwtue4ppjT4a30F7cfFcZshcK1VKB2RH8F4sCeFyaSzzDLJnDL0wOfwfGTVLHrKUU+wIDAQAB'

    # 微信支付
    WEI_XIN = {
        'app_id': 'wxfb58224301433ad6',
        'mch_id': '1525953151',
        'mch_key': 'f3713c60b265730f56b822286724a78e',
        'notify_url': '{}/callback/weixin-recharge/'.format(PAY_HOST),
    }

    # 微信小程序
    MINI_APP_ID = "wxe8eaaa37cd442ff9"
    MINI_APP_SECRET = "eec6f8c6dfae6a56bcb1b4525250129b"

    # 设备
    QR_CODE_PRIVATE_KEY = 'MIICXAIBAAKBgQDX0gNlvY+fFSLK3hKiakBWhqQakIed4HwohcdyZTnUEBJlTQ+CmjOYVlp8ZbmArJxSWAxVrmog9bKTYOP3DWTqP4llQZA+reuUanr94dM0mZfH6jIuJwn0RpZpCUBG20yitGirylWb71gsGVFLhHS0j2RlsYj0YxNFX2N/07SEdwIDAQABAoGAc8GJ3vT4ZnwAqEzKM+DHV2Fp/XGNu8ke7uEqI5pVlP91zm2xpvwsNkYCzHwHLhPm2GevXflppPoDaPbr7qN5fwqlQmD3xOD9QtE8r5U8mbHIsC8ABJfgX3eu3dpER2CgV2+ytdt1Iy2w6p5fRgXMTVAMFd98jXDTdvU6OfpqC9ECQQDrnJhJuqJhadJhwP85NMiVNBCZqRT7tLfJjPpD2vqu6h06VhJCbkNWm0s/NVtmP4qrvdevZJAFnUqkyyrbGFtfAkEA6n79S6i8EYd59Y/I2nna7NOf9BP+KGuIrm1DJyyrKD4xqlPuJjYc6FMDKNK4bsSzaLhgYIZl6eAMc0mD54+F6QJBAOAzbCrEoV4nD54bxAIQu0pXd/Bwl9oJFtaBA2jsiJ1HhDaNzuRN/l/8eHcWc/nxPyi8BvEMtYvSKER2XDqOi+sCQBQ1fX7Xu92G32vaSGULu2JNmqteTbkOC2l84RyvLND7CyyyrwN8BmG/RbZu8pYZPZz4xtWKv524QVpuK3/5ToECQHFJ+JlcPDUciNnnPq4N5Zf9UaOf8iZDpNoW97vN+927X3EQer/CK+LsyNFA3tfArsGHQg+b2dvrN5RoU1zKWQg='
    SCAN_API_KEY = '7af61707e48da90f44b87aad508933d6'  # 終端上传订单数据验证签名中加的盐
    QR_AES_KEY = '202cb962ac59075b964b07152d234b70'  # 加密用戶id
    QR_CODE_TYPE = 'won://'  # won 在线 woff 离线

    # 手机验证码
    ALIYUN_VERIFY_CODE = {
        'accessKeyId': 'LTAIHTcfamNy7bzi',
        'accessSecret': 'wVcKfAmvCL1hbSazwW8olsAFpQWEHF',
        'SignName': '无感行',
        'register_template_code': 'SMS_160856297',
        'password_template_code': 'SMS_161593733',
        'login_template_code': 'SMS_161570314',
    }

    # 百度人脸识别
    BAIDU_APP_ID = '16019070'
    BAIDU_API_KEY = '8NKZFsIy7on2pBUj7zB65Hlq'
    BAIDU_SECRET_KEY = '1tVgfs6uUIb9vDOFwAMLhX7PBBW0fr8G'
    BAIDU_GROUP_ID = "test"

    # 临时目录
    TEMP_DIR = '/data/temp'

    REDIS_DB = 3