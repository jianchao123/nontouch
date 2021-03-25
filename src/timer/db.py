# coding: utf-8
import time
import traceback
from functools import wraps
from decimal import Decimal
import MySQLdb
import redis
from DBUtils.PooledDB import PooledDB
from redis import ConnectionPool
from timer import config
from timer import tools

# main
logger = tools.get_logger(config.log_path)

# mysql
mysql_pool = PooledDB(MySQLdb, 5, **config.mysql_conf)

# redis
rds_pool = ConnectionPool(**config.redis_conf)
rds_conn = redis.Redis(connection_pool=rds_pool)


# 事务装饰器
def transaction(is_commit=False):
    def _transaction(func):
        @wraps(func)
        def __transaction(self, *args, **kwargs):
            mysql_conn = None
            mysql_cur = None
            try:
                mysql_conn = mysql_pool.connection()
                mysql_cur = mysql_conn.cursor()
                result = func(self, mysql_cur, *args, **kwargs)
                if is_commit:
                    mysql_conn.commit()
                return result
            except:
                if mysql_conn:
                    mysql_conn.rollback()
                # 记录日志
                logger.error(traceback.format_exc())
            finally:
                if mysql_cur:
                    mysql_cur.close()
                if mysql_conn:
                    mysql_conn.close()

        return __transaction
    return _transaction


class MysqlDbUtil(object):

    def __init__(self, mysql_cur):
        self.mysql_cur = mysql_cur

    def get(self, sql):
        self.mysql_cur.execute(sql)
        result = self.mysql_cur.fetchone()
        return result

    def query(self, sql):
        self.mysql_cur.execute(sql)
        result = self.mysql_cur.fetchall()
        return result

    def insert(self, data, table_name=None):
        keys = ""
        values = ""
        time_list = ["now()", "NOW()", "current_timestamp",
                     "CURRENT_TIMESTAMP", "null"]
        for k, v in data.items():
            keys += k + ","
            if isinstance(v, (int, float, long, Decimal)) or \
                            v in time_list or "str_to_date" in v:
                values += str(v) + ","
            else:
                values += "'" + str(v) + "'" + ","

        keys = keys[:-1]
        values = values[:-1]

        sql = "insert into {}({}) values({})".format(table_name, keys, values)
        self.mysql_cur.execute(sql)

    def update(self, data, table_name=None):
        sql = "UPDATE {} SET ".format(table_name)
        for k, v in data.iteritems():
            if k != '`id`':
                if isinstance(v, (int, float, long, Decimal)):
                    sql += k + "=" + str(v) + ","
                elif v in ["now()", "NOW()", "current_timestamp",
                           "CURRENT_TIMESTAMP"]:
                    sql += k + "=" + v + ","
                else:
                    sql += k + "=" + "'" + v + "'" + ","
        sql = sql[:-1] + " WHERE `id` = {}".format(data["`id`"])
        self.mysql_cur.execute(sql)
        return sql