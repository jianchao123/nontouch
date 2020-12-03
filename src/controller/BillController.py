# coding:utf-8
try:
    from flask.blueprints import Blueprint

    from core.framework import get_require_check_with_permissions, \
        post_require_check_with_permissions
    from core.AppError import AppError
    from utils.defines import SubErrorCode, GlobalErrorCode

    from service.BillService import BillService
except:
    import traceback
    print traceback.format_exc()

try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('BillController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/bill/list', methods=['GET'])
@get_require_check_with_permissions([])
def bill_list_api(user_id, company_id, args):
    """
发票列表
发票列表，需要先登录
---
tags:
  - 财务管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: status
    in: query
    type: integer
    description: 状态 1待开票 2已开票
  - name: mobile
    in: query
    type: string
    description: 手机号
  - name: offset
    in: query
    type: integer
    description: OFFSET
  - name: limit
    in: query
    type: integer
    description: LIMIT

responses:
  200:
    description: 正常返回http code 200
    schema:
      properties:
        detail:
          type: string
          description: 错误消息
        code:
          type: integer
          description: 状态
        data:
          type: object
          properties:
            id:
              type: integer
              description: PK
            headline:
              type: integer
              description: 抬头
            headline_type:
              type: integer
              description: 抬头类型
            bank_name:
              type: integer
              description: 银行名字
            bank_account:
              type: integer
              description: 银行帐号
            email:
              type: integer
              description: 邮箱
            bill_no:
              type: integer
              description: 发票号
            pub_date:
              type: integer
              description: 开票日期
            enterprise_name:
              type: integer
              description: 企业名字
            enterprise_address:
              type: integer
              description: 企业地址
            enterprise_phone:
              type: integer
              description: 企业手机号
            status:
              type: integer
              description: 状态 1待开票 2已开票
            user_id:
              type: integer
              description: 用户id
            user_phone:
              type: integer
              description: 用户号码

    """
    status = args.get('status', None)
    mobile = args.get('mobile', None)
    offset = int(args['offset'])
    limit = int(args['limit'])
    return BillService.bill_list(company_id, status, mobile, offset, limit)


@bp.route('/bill/invoicing/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def bill_invoicing_api(user_id, company_id, args, pk):
    """
开具发票
开具发票，需要先登录
---
tags:
  - 财务管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: pk
    in: path
    type: integer
    description: PK
responses:
  200:
    description: 正常返回http code 200
    schema:
      properties:
        detail:
          type: string
          description: 错误消息
        code:
          type: integer
          description: 状态
        data:
          type: object
          properties:
            id:
              type: integer
              description: PK

    """
    ret = BillService.bill_invoicing(pk)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.STATUS_ERR)
    return ret