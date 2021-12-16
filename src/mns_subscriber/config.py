# coding:utf-8
import os
import configparser

project_name = "nontouch_1"
project_dir = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))))
env_dist = os.environ
config_name = env_dist.get('NONTOUCH_1_ENV')

if config_name == 'PRO':
    setting_file = 'setting_pro.ini'
elif config_name == 'TEST':
    setting_file = 'setting_test.ini'
else:
    setting_file = 'setting_dev.ini'


class MyConfigParser(configparser.ConfigParser):

    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)

    # 这里重写了optionxform方法，直接返回选项名
    def optionxform(self, optionstr):
        return optionstr


config = MyConfigParser()
real_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), setting_file)
config.read(real_path, encoding='utf-8')
secs = config.sections()
for section in secs:
    kvs = config[section].items()
    globals().update(kvs)
    # for k, v in kvs:
    #     print k, v

config_namespace = globals()
redis_conf = dict(host=config_namespace['redis_host'],
                  port=config_namespace['redis_port'],
                  db=config_namespace['redis_db'],
                  decode_responses=True)
mysql_conf = dict(host=config_namespace['mysql_host'],
                  db=config_namespace['mysql_db'],
                  port=int(config_namespace['mysql_port']),
                  user=config_namespace['mysql_user'],
                  passwd=config_namespace['mysql_passwd'],
                  charset="utf8")
print mysql_conf
print config_name
