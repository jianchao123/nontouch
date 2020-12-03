# coding:utf-8
import datetime
import json
import random
import string
import decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


def time_ago(days=0, hours=0, minutes=0, seconds=0):
    now = datetime.datetime.now()
    timedelta_time = datetime.timedelta(
        days=days, hours=hours, minutes=minutes, seconds=seconds)
    return now - timedelta_time


def five_minutes_ago():
    return time_ago(minutes=5)


def get_now_date():
    return datetime.datetime.now().strftime('%Y%m%d')


def randomDigit(length=6):
    return ''.join(random.choice(string.digits) for i in range(length))


def _build_order_no(user_id):
    # 20190101 + 0 + 12345 + 00000  = 19 位
    result = '{0}{1}{2}{3}'.format(
        get_now_date(), randomDigit(1), user_id[-5:], randomDigit(5))
    return result


def build_recharge_order_no(user_id):
    return _build_order_no(str(user_id))


def build_pay_order_no(user_id):
    return _build_order_no(str(user_id))
