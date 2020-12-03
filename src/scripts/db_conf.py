# coding:utf-8
import os

project_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(project_dir)
project_dir = os.path.dirname(project_dir)
project_name = "nontouch_1"
env_dist = os.environ
env = env_dist.get('NONTOUCH_1_ENV')
if env == "TEST":
    log_path = "/data/logs/{}/mns".format(project_name)
    url = ""

    mysql_host = '127.0.0.1'
    mysql_db = "nontouch_1"
    mysql_port = 3306
    mysql_user = "bus"
    mysql_passwd = "qwe123123"

elif env == "PRO":
    log_path = "/data/logs/{}/mns".format(project_name)
    url = ""

    mysql_host = '47.108.201.70'
    mysql_db = "nontouch_1"
    mysql_port = 3306
    mysql_user = "root"
    mysql_passwd = "kIhHAWexFy7pU8qM"
else:
    log_path = project_dir + "/logs/mns"
    url = ""

    mysql_host = '127.0.0.1'
    mysql_db = "wuganxing_1"
    mysql_port = 3306
    mysql_user = "root"
    mysql_passwd = "kIhHAWexFy7pU8qM"

redis_conf = dict(host="127.0.0.1", port=6379, db=0, decode_responses=True)
mysql_conf = dict(host=mysql_host, db=mysql_db, port=mysql_port,
                  user=mysql_user, passwd=mysql_passwd, charset="utf8")
