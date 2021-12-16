# coding:utf-8
import os
from config.default import Config

project_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(project_dir)
project_dir = os.path.dirname(project_dir)


class DevelopmentConfig(Config):
    """
    开发环境配置数据
    """

    # Flask config
    DEBUG = True

    # Mysql
    SQLALCHEMY_DATABASE_URI = \
        'mysql://root:kIhHAWexFy7pU8qM@127.0.0.1/wuganxing_1'

    LOG_PATH = '/home/jianchao/code/nontouch_1/logs/main'

    # 阿里云OSS
    OSS_BUCKET = "wgxing-dev"
    OSS_REGION = "oss-cn-beijing"
    OSS_POINT = "oss-cn-beijing.aliyuncs.com"
    OSS_ALL_KEY = "LTAI5tHYr3CZ59HCRLEocbDG"  # 所有权限
    OSS_ALL_SECRET = "BMRI8WzUVMRbS6LHPM3bIiadWIPE8c"

    PAY_HOST = 'https://ngrokpay.wgxing.com'

    # 支付宝支付
    APP_ID = '2019121169830445'
    RechargeUrl = '/callback/ali-recharge/'
    NOTIFY_URL = PAY_HOST + RechargeUrl
    ALIPAY_GATEWAY = 'https://openapi.alipay.com/gateway.do'
    APP_PRIVATE_KEY = 'MIIEogIBAAKCAQEAoeQqNeZVf40SSJKNBLDF7KMNV8H5jPRoZ8Nbps2jtGT/6iCT9n9Qzs4ihHkCZeDMeW6Peh4otCDHCNV1a9K3WGsGP12INyd8V2VQ7QJ59TsaEnbQvFWHPyTWtU9rsMIfpyqwiO7gMS7LBMGNBVjrdGyJroMierS4nue7vQokFLAEbgkQW5WLRXBppdhlhygAdbx43aSyG67P3Zs/ptqZ+q7wbwhThFstE4V0VG39z7KHnKhle64+AwEvjEEEux7UekFZxyjjTn0VYP+yFxTdmMXvgEhiBWAEje5xTHhiO8iNxN0f7amUk5HTZhJhBQL+9VJhmBd6n+w1ea9rofBHPwIDAQABAoIBABxNJ/fuQWof/l9Dh3WXdbJtuspptbenjoz9QQuDDahes8J5WYSRM05ECRLBmOK4juZ3pouBtDnxNPpdXr6vwq+pXhk7v7FsrLcWljQo56swXtl1ff4+sXsfdI2Tyc7H0QLHWr9Fi1ntxT4anA2gQuFCjDs+34s2BsR43IAqwq3+5DOMYmZLPZCPHFxKyLQ36xAlOUs+pqzngcXpAdRJJbmQ9RBp+/3kO+2j3jvFawOyjPClQKWlE24fyZNPbdgJ2B151C846MxemSQP7r9Gtm0Tiob8aTUwJA+xELTBfXRjF5s54WOS8HfsBoELyuDg2NaECBW3IYcAUO5LTxtVgkkCgYEA1dH3MuLuhmjIrpSyKYruR+pYLi6s24FHLJOD28kqC0DJII0/UYNTGlk6a3waayfLXR8uJcubIGj6BGhnTRAqBdbtuwboYmJQcA96kU1Om/mOFODoYNUnADJTd8f6+e/8ZQeX2Gw4mqHqm3GqCT6rrfOF3k5iofK96i5VgC2yCcUCgYEAwdPC5q80A/NGZnZG5uXM1Ipm9pdIxYUEZCKAgQqOy3yuXIgjZ37CLxAwiXH5dm6qk3W4P30uJpRkcNo5ulxsMKIqfdveGSvTJR0e6BiBglvC2FqfZDSYLSPgJORdiiDW3L0l5N4BxGjqqrbMIn2duuOdTtnpmJyxtAJNTvvtUTMCgYA1KfKj1WbnRpB3UAOIbsHWYb8xJGvYXCl9PORxNnBcwewASv5uXw+/omXzKbVL5WYcLk+EGD7m7RMVG3xr3dQFBa6wbQREyhsj8cVQ8X7VK1SXfmBpCzaaRukYBEIz+OaxnBS2PBpK4G173uQfTlTTeJRVdPnzOG7eFk0uBK6a3QKBgEtN8K0baMQYIkPws/9FTN1OoE4x3K4QzfHxjaeU6IGagUumAMtW7i7GxXTA+UDQIimEVP8lrWaDxLorrr3+5nHGr2eSoql442HJ/JYD3108NWlFXCPcYzs2cwEiUE04EQJV4oEW1+ztLi8BMjI8R6mygQ1/kEggqNHdCxgivMMNAoGAfZyo5mnwiCOWshlg4/vYmQQuhVP+b8ZQDxZkj84Q5/ARqsZ5WIzcpZWU4xaviBO6hUaxyDv/evd00CanUCKF7t8XrHkMI6MsqsbRhCuDBSq34878k+svK1GgDoZUdnVH/zkNw/eKReAbmGgmCEEOSnHXEAak7dce/nyPjKR/PFo='
    ALIPAY_PUBLIC_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnUyTSsCGBC+rhqAoGwOXNTRvafK7qRChmJKNLhersqyck+99Mb1xal+iqUEy9qCpDntWa/qB5XHUclRz2MrP//66CJKWAAaU+6zOKTekBuEd83eDedY5nlrBrBcvs2d841dRIvePksEhI9CGt26/d9LlN8o97vrjgiNdKytPOGKdCNF0e998XFWVD1sxvkyFW6ySy2j3BKyL1DVG4brU5KE6jgp782XOIgvPXKn6N2DR/5D69QMijZAQ0UCVsPspVDdC6MfbmjSRJEPP7qsrwtue4ppjT4a30F7cfFcZshcK1VKB2RH8F4sCeFyaSzzDLJnDL0wOfwfGTVLHrKUU+wIDAQAB'
    #ENTERPRISE_PAY_APP_PUB_KEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvYQgbbxbUps9iCeTNTRmdRBbVsr8Ncou3/VHsXxclWYiyQNcdj3gJCDrnvyT2lEMGYaPCDIUDt/fXeRG3Iupu6eSCB/zQCg5mDRRGACDVs0ryWPoMXdks2CTy8pwzj2mIE2egEHS1mCyDnB2aw8Vwct/PGN1RepsZwpRFG7M01Y6HDS+1wFnFIQI5BQQ0yG17PkRenjCQ2JX6CMRw968GqMrtHkxpl+x/rDfUWxFTHmDzybRFOqU4XfDfRuZyy2Iaxi9+SVD3dwra7RXDrprv7WMUk9rYvUGTaQNWVkl54KeOeJ3cBCCavF1kUdnXtBYnnm4/V8ubkpSli5ui/pTFwIDAQAB"
    #ENTERPRISE_PAY_APP_PRI_KEY = "MIIEpAIBAAKCAQEAvYQgbbxbUps9iCeTNTRmdRBbVsr8Ncou3/VHsXxclWYiyQNcdj3gJCDrnvyT2lEMGYaPCDIUDt/fXeRG3Iupu6eSCB/zQCg5mDRRGACDVs0ryWPoMXdks2CTy8pwzj2mIE2egEHS1mCyDnB2aw8Vwct/PGN1RepsZwpRFG7M01Y6HDS+1wFnFIQI5BQQ0yG17PkRenjCQ2JX6CMRw968GqMrtHkxpl+x/rDfUWxFTHmDzybRFOqU4XfDfRuZyy2Iaxi9+SVD3dwra7RXDrprv7WMUk9rYvUGTaQNWVkl54KeOeJ3cBCCavF1kUdnXtBYnnm4/V8ubkpSli5ui/pTFwIDAQABAoIBAFXoavrTg2Iy1PW/Ws+nbTprq7vwT9viRtVmzpT6Fs3yepo8V9GRwuUdtzFetXclfiKkCHpimQ0VFp/tNuIKvWo/T8c3FIFkupbwQEJtGRxj7RFhpIOn55IYmWar4e7bq07BYLQrInPjaVN6T3PAZtBuesLZIvQKjBE5b/+fKmIxz4rrjsTglnh+eVoSZUeptZFolwy0phj9+pypoqM/+9qACoHfwOianVtsxlOwQsvEqnYaSCagnsOF+6mm69BGBA2LxZhpZUJRtSby9urmZc1JYOPiEAlZ1NKUh0j0jRv36h5E2Rzm4PiiVvje/HGlrWtR+OEQbG63tS2n8lcnokECgYEA8rYrNP5vC4uFfDPg7gLBBt+7I8T5o8f/bKrNj0LyNFlXfjh997BZPDfcb0MtEQISGeE0KeA6ejjR4RVx0BBEsKUR2Tl6ly07LStmD3CI0lGI5LVYesTF2I86C+yRZcMduSFN9WUnYkE/tmcKPeAiJZ6OZLS3Z1EYtAIqwU/AZ+kCgYEAx+Rfjt/rSvJBBibX+LW1Hy+6AywAxENOEZSkNUkqTmClW1zwntkk+4hanBpSugeKAFPdpGfvuLtKCC+YOxIQwUTof9tals4BVo3/XVE2qQNT/9esjo8jyQW37GutvkbAL1K0FjWDoh1TcYN2OywBhLd4lK4NLBSk8/rtuFeLAv8CgYEA6CRa4R32Ygl5jBkmqx+RNhzppkWxK/iPkoUvhTXX6UAGkiBAQ5a1UwZu3TBYO2tKmtwug1sHM32DKJDVQdc9i+LmVmlGmq/VaNeYj23oP5lioLXewdXREde0AlGro7Riin6TTQIKEE0uPi0Bu7rTjj3AHgxHWxdS1GE6OZkpA3kCgYBJJxqRfwDs/JsvVSfUrSsLrru0TXY6XSdE59Dwb0Y8SMI7HVgxyeXu54fBeSCtU/T9CbQjZqYkROZi+IgNlh7rm/w6TlxotBtpQa4iyIXodH9ZMeTEhz3hY2Zb70w2Rk4vA2VEe3Eg8vqGoEW0gfZMS5ilUM0hRKzZXQuCWwdUoQKBgQCGIqAEKPMX2s66T3r+DtQXy97WfvAdkcrlxBMD3n2FC7RHitEQdIT7x4IRdV6M/FGK4F9rDsNJq1g29/EVRl80ElF1X+lD4flnk16l8DWZZu9VBbyJV9sMMQ9WJ2U+3+3Y1hdx3VFYyCPZLgtgl1p0ZjHPjUDL6Ews1VVFg5MRbA=="


    # 微信支付
    WEI_XIN = {
        'app_id': 'wxfb58224301433ad6',
        'mch_id': '1525953151',
        'mch_key': 'f3713c60b265730f56b822286724a78e',
        'notify_url': '{}/callback/weixin-recharge/'.format(PAY_HOST),
    }

    # 微信小程序
    MINI_APP_ID = "wxe4e34a7e3f11397e"
    MINI_APP_SECRET = "8b92286b253c45b9906494cb797eb573"

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
    BAIDU_APP_ID = '24831558'
    BAIDU_API_KEY = 'Si8bUb5dIqK4ZwtiKL5tFkKP'
    BAIDU_SECRET_KEY = 'XNRNi6MpIZjBqfSN0adcOHIPOk2GQVEk'
    BAIDU_GROUP_ID = 'china'

    # 临时目录

    TEMP_DIR = project_dir + "/src/utils/temp"

    # 公交项目使用redis db3
    REDIS_DB = 3
