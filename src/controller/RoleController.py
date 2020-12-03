# coding:utf-8
try:
    from flask.blueprints import Blueprint
    from core.framework import get_require_check_with_permissions, \
        post_require_check_with_permissions
    from core.AppError import AppError
    from utils.defines import GlobalErrorCode, SubErrorCode

    from service.RoleService import RoleService
except:
    import traceback
    print traceback.format_exc()


try:
    import requests
    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('RoleController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/role/list', methods=['GET'])
@get_require_check_with_permissions([])
def role_list(user_id, company_id, args):
    """

角色列表
角色列表，需要先登录
---
tags:
  - 后台管理
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
              company:
                type: integer
                description: 公司
              describe:
                type: string
                description: 描述
              show_name:
                type: string
                description: 显示的名字
              status:
                type: integer
                description: 1-有效
    """
    offset = int(args['offset'])
    limit = int(args['limit'])
    return RoleService.role_list(company_id, offset, limit)


@bp.route('/role/change/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def role_update(user_id, company_id, args, pk):
    """

修改角色
修改角色，需要先登录
---
tags:
  - 后台管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: pk
    in: path
    type: integer
    required: true
    description: 站点pk
  - name: body
    in: body
    required: true
    schema:
      properties:
        show_name:
          type: string
          required: true
          description: 显示名字
        describe:
          type: string
          required: true
          description: 描述
        company:
          type: integer
          required: false
          description: 公司
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
              description: 修改成功的Id
    """
    show_name = args.get('show_name', None)
    describe = args.get('describe', None)
    ret = RoleService.role_update(pk, show_name, describe)
    if ret == -1:
        raise AppError(GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(GlobalErrorCode.DB_COMMIT_ERR)
    return {'id': ret}


@bp.route('/role/add', methods=['POST'])
@post_require_check_with_permissions([])
def role_add(user_id, company_id, args):
    """

修改角色
修改角色，需要先登录
---
tags:
  - 后台管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: pk
    in: path
    type: integer
    required: true
    description: 站点pk
  - name: body
    in: body
    required: true
    schema:
      properties:
        show_name:
          type: string
          required: true
          description: 显示名字
        describe:
          type: string
          required: true
          description: 描述
        company:
          type: integer
          required: false
          description: 公司
        role_name:
          type: string
          description: 角色CODE  英文字符,大小写均可,长度超过6-10个字符
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
              description: 修改成功的Id
    """
    role_name = args.get('role_name', None)
    show_name = args.get('show_name', None)
    describe = args.get('describe', None)
    ret = RoleService.role_add(company_id, role_name, show_name, describe)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.ROLE_CODE_ALREADY_EXIST)
    return {'id': ret}


@bp.route('/role/delete/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def role_delete(user_id, company_id, args, pk):
    """

删除角色
删除角色，需要先登录
---
tags:
  - 后台管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: pk
    in: path
    type: integer
    required: true
    description: 站点pk

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
              description: 删除成功的Id

    """
    ret = RoleService.role_delete(pk)
    if ret == -1:
        raise AppError(GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(GlobalErrorCode.DB_COMMIT_ERR)
    return {'id': ret}