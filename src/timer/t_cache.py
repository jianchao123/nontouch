# coding:utf-8
import redis
import json
import time
from timer import db
# 自旋锁专用连接
lock_conn = redis.Redis(connection_pool=db.rds_pool)


class CacheUtil(object):
    PERIOD_TARGET_AMOUNTS_KEY = "period:target:amounts:{}"
    PERIOD_COUNTDOWN = "period:countdown:milli:{}"
    TODAY_COUNT = "today:period:count:{}"
    DIALOG_KEY = "dialog:{}"
    OPEN_PRIZE_COUNT = "open:prize:count"

    @staticmethod
    def today_count(today_str):
        """每日周期计数"""
        return db.rds_conn.incr(CacheUtil.TODAY_COUNT.format(today_str))

    @staticmethod
    def set_period_amounts(period_id, amounts):
        """设置周期目标量"""
        db.rds_conn.set(
            CacheUtil.PERIOD_TARGET_AMOUNTS_KEY.format(period_id), amounts)

    @staticmethod
    def get_pttl_expire(period_id):
        """获取周期倒计时毫秒数"""
        return db.rds_conn.pttl(CacheUtil.PERIOD_COUNTDOWN.format(period_id))

    @staticmethod
    def dialog_push(player_pk, data):
        """push一个弹窗"""
        db.rds_conn.lpush(CacheUtil.DIALOG_KEY.format(player_pk),
                       json.dumps(data))

    @staticmethod
    def incr_open_prize_count():
        """递增开奖计数"""
        db.rds_conn.incr(CacheUtil.OPEN_PRIZE_COUNT)

    @staticmethod
    def get_open_prize_count():
        """获取开奖计数"""
        return db.rds_conn.get(CacheUtil.OPEN_PRIZE_COUNT)


class RedisLock(object):

    def __init__(self, key):
        self.rdcon = lock_conn
        self._lock = 0
        self.lock_key = key

    def get_lock(self, timeout=10):
        while self._lock != 1:
            timestamp = time.time() + timeout + 1
            self._lock = self.rdcon.setnx(self.lock_key, timestamp)
            if self._lock == 1 or (time.time() > self.rdcon.get(self.lock_key)
                                   and time.time() > self.rdcon.getset(
                    self.lock_key, timestamp)):
                break
            else:
                time.sleep(0.3)

    def release(self):
        if time.time() < self.rdcon.get(self.lock_key):
            self.rdcon.delete(self.lock_key)


def lock_nonblock(func):
    def __deco(*args, **kwargs):
        lock_key = "nontouch_1:lock:nonblock:{}".format(func.__name__)
        lock_key += ":{}".format(kwargs)
        instance = RedisLock(lock_key)

        instance.get_lock()
        try:
            return func(*args, **kwargs)
        finally:
            instance.release()

    return __deco
