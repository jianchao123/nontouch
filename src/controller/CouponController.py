# coding:utf-8

from flask.blueprints import Blueprint

from core.framework import get_require_check_with_permissions

from service.CouponService import CouponService


try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('CouponController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/coupon/list', methods=['GET'])
@get_require_check_with_permissions([])
def coupon_list(user_id, company_id, args):
    """
优惠券列表
优惠券列表，需要先登录
---
tags:
  - 运营管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: type_id
    in: query
    type: integer
    required: false
    description: 活动类型id
  - name: offset
    in: query
    type: integer
    required: true
    description: OFFSET
  - name: limit
    in: query
    type: integer
    required: true
    description: LIMIT
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
              code:
                type: string
                description: 优惠券码
              face_value:
                type: number
                description: 面值
              get_time:
                type: string
                description: 领取时间
              name:
                type: string
                description: 优惠券名称
              nickname:
                type: string
                description: 用户昵称
              status:
                type: integer
                descriptipn: 状态 1未发放 2已发放 3已使用 4已过期
              use_time:
                type: string
                description: 使用时间

    """
    mobile = args.get('mobile', None)
    type_id = args.get('type_id', None)
    offset = int(args['offset'])
    limit = int(args['limit'])
    return CouponService.coupon_list(mobile, type_id, offset, limit)