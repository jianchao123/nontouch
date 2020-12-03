# coding:utf-8
try:
    from flask.blueprints import Blueprint
    from core.framework import get_require_check_with_permissions
    from service.OrderService import OrderService
except:
    import traceback
    print traceback.format_exc()
try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('OrderController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/order/list', methods=['GET'])
@get_require_check_with_permissions([])
def order_list(user_id, company_id, args):
    """
订单列表
订单列表，需要先登录
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
  - name: mobile
    in: query
    type: string
    description: 手机号
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
              amount:
                type: string
                description: 应支付金额
              bus_id:
                type: string
                description: 车牌号
              company_id:
                type: integer
                description: 公司id
              company_name:
                type: string
                description: 公司名字
              content:
                type: string
                description: 内容
              discount:
                type: number
                description: 折扣金额
              discount_way:
                type: integer
                description: 折扣方式 0.无优惠 1.身份 2.优惠券 3.免费
              order_no:
                type: string
                description: 订单号
              pay_time:
                type: string
                description: 支付时间
              pay_type:
                type: integer
                description: 支付方式(1-支付宝 2-微信 3-银联 4-余额)
              real_amount:
                type: number
                description: 实际支付金额
              route_name:
                type: string
                description: 线路名字
              scan_time:
                type: string
                description: 扫码时间
              status:
                type: integer
                description: 订单状态 1待支付 2成功 3失败
              user_id:
                type: integer
                description: 用户id
              user_mobile:
                type: stirng
                description: 用户手机号
              user_nickname:
                type: string
                description: 用户昵称
              verify_type:
                type: integer
                description: 1无感行二维码 2人脸 3IC卡 4现金 5微信 6支付宝 7银联
    """
    mobile = args.get('mobile', None)
    offset = int(args['offset'])
    limit = int(args['limit'])
    return OrderService.order_list(company_id, mobile, offset, limit)