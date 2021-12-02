# coding:utf-8

from flask.blueprints import Blueprint
from core.framework import get_require_check_with_permissions
from service.TemperatureService import TemperatureService

try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('TemperatureController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/temperature/list', methods=['GET'])
@get_require_check_with_permissions([])
def temperature_list(user_id, company_id, args):
    """
温度列表
温度列表，需要先登录
---
tags:
  - 商家管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: offset
    in: query
    type: integer
    description: offset
  - name: limit
    in: query
    type: integer
    description: limit
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
          type: array
          items:
            properties:
              id:
                type: integer
                description: id
              mobile:
                type: string
                description: 手机号
              temperature:
                type: float
                description: 温度
              up_timestamp:
                type: float
                description: 刷脸时间
              car_no:
                type: string
                description: 车牌
              gps:
                type: string
                description: gps

    """

    offset = int(args['offset'])
    limit = int(args['limit'])
    return TemperatureService.temperature_list(company_id, offset, limit)