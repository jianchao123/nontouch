# coding:utf-8
try:
    from flask.blueprints import Blueprint
    from core.framework import get_require_check_with_permissions, \
        post_require_check_with_permissions
    from core.AppError import AppError
    from utils.defines import GlobalErrorCode, SubErrorCode

    from service.SettlementService import SettlementService
except:
    import traceback
    print traceback.format_exc()
try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('SettlementController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/settlement/list', methods=['GET'])
@get_require_check_with_permissions([])
def settlement_list_api(user_id, company_id, args):
    """
结算列表
结算列表，需要先登录
---
tags:
  - 财务管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: body
    in: body
    required: true
    schema:
      properties:
        offset:
          type: integer
          description: OFFSET
        limit:
          type: integer
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
                description: pk
              create_time:
                type: string
                description: 创建时间
              start_time:
                type: string
                description: 筛选开始时间
              end_time:
                type: string
                description: 筛选结束时间
              status:
                type: integer
                description: 状态 1结算完成 2已打款
              amount:
                type: number
                description: 金额
              company_id:
                type: integer
                description: 公司id
              company_name:
                type: string
                description: 公司名字
              xls_oss_url:
                type: string
                description: xls 文件url


    """
    offset = int(args['offset'])
    limit = int(args['limit'])
    return SettlementService.settlement_list(company_id, offset, limit)


@bp.route('/settlement/add', methods=['POST'])
@post_require_check_with_permissions([])
def settlement_add_api(user_id, company_id, args):
    """
生成结算单
生成结算单，需要先登录
---
tags:
  - 财务管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: body
    in: body
    required: true
    schema:
      required:
        - organization_id
        - user_id
      properties:
        start_time:
          type: string
          description: 开始时间
        end_time:
          type: string
          description: 结束时间
        company_pk:
          type: integer
          description: 公司id

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
    start_time = args['start_time']
    end_time = args['end_time']
    company_pk = args['company_pk']
    ret = SettlementService.settlement_add(
        company_id, start_time, end_time, company_pk)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret


@bp.route('/settlement/filtrate', methods=['GET'])
@get_require_check_with_permissions([])
def settlement_filtrate_api(user_id, company_id, args):
    """
结算-筛选订单
结算-筛选订单，需要先登录
---
tags:
  - 财务管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: body
    in: body
    required: true
    schema:
      required:
        - organization_id
        - user_id
      properties:
        start_time:
          type: string
          description: 开始时间
        end_time:
          type: string
          description: 结束时间
        offset:
          type: integer
          description: OFFSET
        limit:
          type: integer
          description: LIMIT
        company_pk:
          type: integer
          description: 公司id

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
            count:
              type: integer
              description: 订单数量
            statistics:
              type: object
              properties:
                order_number:
                  type: string
                  description: 订单数量
                time_between:
                  type: string
                  description: 时间范围
                total_amount:
                  type: string
                  description: 总金额
                real_amount:
                  type: string
                  description: 实付金额
                discount_amount:
                  type: string
                  description: 折扣金额
            results:
              type: array
              items:
                properties:
                  id:
                    type: integer
                    description: pk
                    amount:
                      type: number
                      description: 结算金额
                    discount:
                      type: number
                      description: 折扣金额
                    discount_way:
                      type: integer
                      description: 折扣方式 0无优惠 1身份 2优惠券 3免费
                    order_no:
                      type: string
                      description: 订单号
                    pay_time:
                      type: string
                      description: 支付方式
                    pay_type:
                      type: integer
                      description: 支付类型 支付方式 1支付宝 2微信 3银联 4余额
                    real_amount:
                      type: number
                      description: 实付金额
                    scan_time:
                      type: string
                      description: 扫码时间
                    status:
                      type: integer
                      description: 订单状态 1待支付 2成功 3失败
                    user_mobile:
                      type: string
                      description: 用户手机号



    """
    start_time_str = args['start_time']
    end_time_str = args['end_time']
    offset = int(args['offset'])
    limit = int(args['limit'])
    company_pk = int(args['company_pk'])
    return SettlementService.settlement_filtrate(
        start_time_str, end_time_str, company_pk, offset, limit)


@bp.route('/settlement/retrieve/<int:pk>', methods=['GET'])
@get_require_check_with_permissions([])
def settlement_retrieve_api(user_id, company_id, args, pk):
    """
结算检索
结算检索，需要先登录
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
    reuiqred: true
    description: PK
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
                description: pk
              create_time:
                type: string
                description: 创建时间
              start_time:
                type: string
                description: 开始时间
              end_time:
                type: string
                description: 结束时间
              status:
                type: integer
                description: 状态 1结算完成 2已打款
              amount:
                type: number
                description: 结算金额
              company_id:
                type: integer
                description: 公司id
              company_name:
                type: string
                description: 公司名字
              xls_oss_url:
                type: string
                description: excel url
              orders:
                type: array
                items:
                  properties:
                    settlement_detail_id:
                      type: integer
                      description: 结算详情Id
                    order_id:
                      type: integer
                      description: 订单Id
                    order_no:
                      type: string
                      description:  订单号
                    pay_time:
                      type: string
                      description: 支付时间
                    amount:
                      type: number
                      description: 订单金额
                    discount:
                      type: number
                      description: 折扣金额
                    real_amount:
                      type: number
                      description: 实付金额
                    discount_way:
                      type: integer
                      description: 折扣方式 0无优惠 1身份 2优惠券 3免费

    """
    return SettlementService.settlement_retrieve(pk)