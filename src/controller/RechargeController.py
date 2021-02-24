# coding:utf-8

from flask.blueprints import Blueprint
from core.framework import get_require_check_with_permissions
from service.RechargeService import RechargeService

try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('RechargeController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/recharge/list', methods=['GET'])
@get_require_check_with_permissions([])
def recharge_list(user_id, company_id, args):
    """
    充值列表
    充值列表，需要先登录
    ---
    tags:
      - 财务管理
    parameters:
      - name: token
        in: header
        type: string
        required: true
        description: TOKEN
      - name: offset
        in: query
        type: integer
        required: true
        description: offset
      - name: limit
        in: query
        type: integer
        required: true
        description: limit
      - name: pay_type
        in: query
        type: integer
        description: 支付方式(1-支付宝 2-微信 3-银联 4-余额)
      - name: status
        in: query
        type: integer
        description: 订单状态(1:待支付,2:成功,3:失败)
      - name: find_str
        in: query
        type: string
        description: 订单或者手机号
      - name: user_id
        in: query
        type: integer
        description: 用户id
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
                    description: PK
                  body:
                    type: string
                    description: BODY
                  create_time:
                    type: string
                    description: 创建时间
                  name:
                    type: string
                    description: 名字
                  order_no:
                    type: string
                    description: 下单号
                  pay_time:
                    type: string
                    description: 支付时间
                  pay_type:
                    type: integer
                    description: 支付方式(1-支付宝 2-微信 3-银联 4-余额)
                  remark:
                    type: string
                    description: 备注
                  status:
                    type: integer
                    description: 订单状态(1:待支付,2:成功,3:失败)
                  trade_no:
                    type: string
                    description: 支付宝交易凭证号
                  user_id:
                    type: integer
                    description: 用户id
                  username:
                    type: string
                    description: 用户名

    """
    offset = args['offset']
    limit = args['limit']
    find_str = args.get('find_str', None)
    pay_type = args.get('pay_type', None)
    status = args.get('status', None)
    user_id = args.get('user_id', None)
    return RechargeService.recharge_list(
        company_id, find_str, pay_type, status, offset, limit, user_id)
