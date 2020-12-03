# coding:utf-8
try:
    from flask.blueprints import Blueprint
    from core.framework import get_require_check_with_permissions,\
        post_require_check_with_permissions
    from core.AppError import AppError
    from utils.defines import SubErrorCode, GlobalErrorCode
    from service.CompanyService import CompanyService
except:
    import traceback
    print traceback.format_exc()
try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('CompanyController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/company/list', methods=['GET'])
@get_require_check_with_permissions([])
def company_list(user_id, company_id, args):
    """
公交公司列表
公交公司列表，需要先登录
---
tags:
  - 商家管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: name
    in: query
    type: string
    description: 公司名称
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
              name:
                type: string
                description: 公司名称
              house_number:
                type: string
                description: 门牌号
              permissions:
                type: string
                description: 权限数组字符串
              status:
                type: integer
                description: 状态 1启用中 2禁用中
              create_time:
                type: string
                description: 创建时间
              line_nos:
                type: string
                description: 该公司所有的公交线路,逗号分割
              logo:
                type: string
                description: 公司Logo
              username:
                type: string
                description: 管理员帐号
              mobile:
                type: string
                description: 管理员手机号
              province_id:
                type: integer
                description: 省id
              area_id:
                type: integer
                description: 区id
              city_id:
                type: integer
                description: 城市id

    """
    name = args.get('name', None)
    offset = args.get('offset')
    limit = args.get('limit')
    return CompanyService.company_list(company_id, name, offset, limit)


@bp.route('/company/change/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def company_update(user_id, company_id, args, pk):
    """

修改公交公司
修改公交公司，需要先登录
---
tags:
  - 商家管理
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
    description: 公司pk
  - name: body
    in: body
    required: true
    schema:
      properties:
        area:
          type: integer
          description: 区id
        city:
          type: integer
          description: 市id
        province:
          type: integer
          description: 省id
        house_number:
          type: string
          description: 门牌号
        mobile:
          type: string
          description: 手机号
        name:
          type: string
          description: 公司名称
        permissions:
          type: string
          description: 权限 array
        username:
          type: string
          description: 管理员用户名
        password:
          type: string
          description: 管理员密码
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
    area_id = args.get('area', None)
    city_id = args.get('city', None)
    province_id = args.get('province', None)
    house_number = args.get('house_number', None)
    mobile = args.get('mobile', None)
    name = args.get('name', None)
    new_permissions = args.get('permissions', None)
    username = args.get('username', None)
    password = args.get('password', None)

    ret = CompanyService.company_update(
        company_id, pk, area_id, city_id, province_id, house_number,
        mobile, name, new_permissions, username, password)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.PERMISSION_PRIVILEGE_SET)
    return ret


@bp.route('/company/add', methods=['POST'])
@post_require_check_with_permissions([])
def company_add(user_id, company_id, args):
    """

添加公交公司
添加公交公司，需要先登录
---
tags:
  - 商家管理
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
        area:
          type: integer
          description: 区id
        city:
          type: integer
          description: 市id
        province:
          type: integer
          description: 省id
        house_number:
          type: string
          description: 门牌号
        mobile:
          type: string
          description: 手机号
        name:
          type: string
          description: 公司名称
        permissions:
          type: string
          description: 权限 array
        username:
          type: string
          description: 管理员用户名
        password:
          type: string
          description: 管理员密码
        line_nos:
          type: string
          description: 该公司的所有线路,逗号分割 例 1,25,125,89
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
              description: 添加成功的Id
    """
    area_id = args.get('area')
    city_id = args.get('city')
    province_id = args.get('province')
    house_number = args.get('house_number')
    mobile = args.get('mobile')
    name = args.get('name')
    line_nos = args.get('line_nos')
    permissions = args.get('permissions')
    username = args.get('username')
    password = args.get('password')

    ret = CompanyService.company_add(
        company_id, area_id, city_id, province_id, house_number,
        line_nos, mobile, name, password, permissions,
        username)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.PERMISSION_PRIVILEGE_SET)
    return ret


@bp.route('/company/disable/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def company_disable(user_id, company_id, args, pk):
    """

禁用公交公司
禁用公交公司，需要先登录
---
tags:
  - 商家管理
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
    description: 公司pk

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
    ret = CompanyService.company_disable(pk)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == 3:
        raise AppError(*SubErrorCode.STATUS_ERR)
    return ret


@bp.route('/company/enable/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def company_enable(user_id, company_id, args, pk):
    """

启用公交公司
启用公交公司，需要先登录
---
tags:
  - 商家管理
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
    description: 公司pk

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
    ret = CompanyService.company_enable(pk)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == 3:
        raise AppError(*SubErrorCode.STATUS_ERR)
    return ret