# coding:utf-8
import os


class Config(object):
    """
    默认配置数据
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Flask config
    DEBUG = False
    TESTING = False
    SECRET_KEY = '‭1DF5E76‬'

    # mongodb config
    # ex: mongodb://root:aaa2016@localhost:27017/mongo_test
    # MONGO_URI = os.environ.get('APP_MONGO_URI')

    # App config
    APP_SERVICE_NAME = 'nontouch_1'
    APP_LOG_LEVEL = 'info'

    # OpenSearch configure
    OPENSEARCH_APP_KEY = 'LTAIikXs0Aj9UinP'
    OPENSEATCH_APPSECRET = 'BfERDEYFxw3rYY6vHHLnhJ0j9lZrKB'
    OPENSEATCH_BASE_URL = 'http://opensearch-cn-hangzhou.aliyuncs.com'

    # Mysql
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_POOL_RECYCLE = 360
    SQLALCHEMY_POOL_TIMEOUT = 10

    # Redis
    REDIS_HOST = 'localhost'
    REDIS_PORT = '6379'
    REDIS_PASSWORD = ''

    # encrypt
    SALT = "LFLgi9VU"

    RSA_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, "rsa_doc/rsa_private_key.pem")
    RSA_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, "rsa_doc/rsa_public_key.pem")