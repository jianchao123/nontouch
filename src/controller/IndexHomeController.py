# coding:utf-8

from datetime import timedelta
from collections import defaultdict
from flask.blueprints import Blueprint
from core.framework import get_require_check_with_permissions
from core.AppError import AppError
from utils.defines import GlobalErrorCode, SubErrorCode
from service.IndexHomeService import IndexHomeService
from ext import conf

try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('IndexHomeController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/index', methods=['GET'])
@get_require_check_with_permissions([])
def index_home_api(user_id, company_id, args):
    """
主页数据
主页数据，需要先登录
---
tags:
  - 主页
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN

responses:
  200:
    description: 正常返回http code 200
    schema:
      properties:
        msg:
          type: string
          description: 错误消息
        status:
          type: integer
          description: 状态
        data:
          type: object
          properties:
            id:
              type: integer
              description: pk
    """
    from datetime import date

    today = date.today()
    yesterday = today - timedelta(days=1)

    today_str = today.strftime("%Y-%m-%d")
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    today_begin = today_str + " 00:00:00"
    today_end = today_str + " 23:59:59"

    yesterday_begin = yesterday_str + " 00:00:00"
    yesterday_end = yesterday_str + " 23:59:59"

    data = defaultdict()
    # 注册用户
    data["signup_user"] = IndexHomeService.signup_user_data(
        today_begin, today_end, yesterday_begin,
        yesterday_end, company=company_id)
    # 乘车人次
    data["bus_take_number"] = IndexHomeService.bus_take_number(
        today_begin, today_end, yesterday_begin,
        yesterday_end, company=company_id)
    # 订单总额
    data["order_total_amount"] = IndexHomeService.order_total_amount(
        today_begin, today_end, yesterday_begin,
        yesterday_end, company=company_id)
    # 充值总额
    data["recharge_total_amount"] = IndexHomeService.recharge_total_amount(
        today_begin, today_end, yesterday_begin,
        yesterday_end, company_id)
    # 近七日注册用户
    data["signup_user_histogram"] = IndexHomeService.signup_user_histogram(
        today, company_id)
    # 近七日乘车人数
    data["take_bus_histogram"] = IndexHomeService.take_bus_histogram(
        today, company_id)
    # 近七日订单额
    data["order_total_amount_histogram"] = \
        IndexHomeService.order_total_amount_histogram(
            today, company_id)
    # 线路流量排行
    data["route_rank_histogram"] = \
        IndexHomeService.route_rank_histogram(today, company_id)
    print(data)
    return data
