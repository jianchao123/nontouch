# coding:utf-8
try:
    from flask.blueprints import Blueprint

    from core.framework import get_require_check_with_permissions, \
        post_require_check_with_permissions
    from core.AppError import AppError
    from utils.defines import SubErrorCode, GlobalErrorCode

    from service.IdentityService import IdentityService
except:
    import traceback
    print traceback.format_exc()
try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('IdentityController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/identity/list', methods=['GET'])
@get_require_check_with_permissions([])
def identity_list_api(user_id, company_id, args):
    """
身份列表
身份列表，需要先登录
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
          type: object
          properties:
            id:
              type: integer
              description: PK
            name:
              type: string
              description: 身份名字
            company_id:
              type: integer
              description: 公司id
            company_name:
              type: string
              description: 公司名字
            description:
              type: string
              description: 描述
            months:
              type: integer
              description: 月份
            number:
              type: integer
              description: months内免费乘坐次数
            status:
              type: integer
              description: 1使用中 10已删除
            discount_rate:
              type: number
              description: 折扣比率
            create_time:
              type: string
              description: 创建时间
    """
    offset = args['offset']
    limit = args['limit']
    return IdentityService.identity_list(company_id, offset, limit)


@bp.route('/identity/delete/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def identity_delete_api(user_id, company_id, args, pk):
    """
删除身份
删除身份，需要先登录
---
tags:
  - 运营管理
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
    ret = IdentityService.identity_delete(pk)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.CERT_IDENTITY_ALREADY_BINDING_USER)
    return ret


@bp.route('/identity/add', methods=['POST'])
@post_require_check_with_permissions([])
def identity_add_api(user_id, company_id, args):
    """
添加身份
添加身份，需要先登录
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
        description:
          type: integer
          description: 描述
        discount_rate:
          type: integer
          description: 折扣比率 例 0.02
        months:
          type: integer
          description: 月份
        name:
          type: integer
          description: 身份名称
        number:
          type: integer
          description: 在months内可以免费乘坐的次数

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
    description = args['description']
    discount_rate = args['discount_rate']
    months = args['months']
    name = args['name']
    number = args['number']
    ret = IdentityService.identity_add(
        company_id, description, discount_rate, months, name, number)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.CERT_IDENTITY_REPEAT)
    return ret
