# coding:utf-8

from flask.blueprints import Blueprint

from core.framework import get_require_check_with_permissions, \
    post_require_check_with_permissions
from core.AppError import AppError
from utils.defines import SubErrorCode, GlobalErrorCode

from service.PassengerIdentityService import PassengerIdentityService

try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('PassengerIdentityController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/passengeridentity/list', methods=['GET'])
@get_require_check_with_permissions([])
def passenger_identity_list_api(user_id, company_id, args):
    """
乘客的身份列表
乘客的身份列表，需要先登录
---
tags:
  - 运营管理
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
        status:
          type: integer
          description: 状态 1生效中 2已过期 10已删除
        identity_id:
          type: integer
          description: 身份id
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
        detail:
          type: string
          description: 错误消息
        code:
          type: integer
          description: 状态
        data:
          type: array
          items:
            properties:
              id:
                type: integer
                description: PK
              company_name:
                type: string
                description: 公司名字
              user_mobile:
                type: string
                description: 用户手机号
              user_id:
                type: integer
                description: 用户id
              identity_id:
                type: integer
                description: 身份id
              identity_name:
                type: string
                description: 身份名字
              status:
                type: integer
                description: 状态 1生效中 2已过期 10已删除
              section_begin_time:
                type: string
                description: 区间次数开始时间
              section_end_time:
                type: string
                description: 区间次数结束时间
              end_time:
                type: string
                description: 身份截止时间
              residue_number:
                type: integer
                description: 剩余时间
              discount_rate:
                type: number
                description: 该身份折扣比率

    """
    status = args.get('status', None)
    identity_id = args.get('identity_id', None)
    offset = int(args['offset'])
    limit = int(args['limit'])
    return PassengerIdentityService.passenger_identity_list(
        company_id, status, identity_id, offset, limit)


@bp.route('/passengeridentity/delete', methods=['POST'])
@post_require_check_with_permissions([])
def passenger_identity_delete_api(user_id, company_id, args):
    """
删除乘客的身份
删除乘客的身份，需要先登录
---
tags:
  - 运营管理
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
        pks:
          type: string
          required: true
          description: id字符串 逗号分割

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
    pks = args['pks']
    ret = PassengerIdentityService.passenger_identity_delete(pks)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.STATUS_ERR)
    return ret