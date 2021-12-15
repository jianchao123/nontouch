# coding:utf-8
import redis
from redis import ConnectionPool
import config as conf


# redis
rds_pool = ConnectionPool(**conf.redis_conf)
rds_conn = redis.Redis(connection_pool=rds_pool)

