# coding:utf-8

from flask.blueprints import Blueprint
from core.framework import get_require_check_with_permissions, \
    post_require_check_with_permissions, post_require_check
from core.AppError import AppError
from utils.defines import GlobalErrorCode, SubErrorCode
from service.AdminUserService import AdminUserService
from ext import conf
from utils.rest import gen_token, md5_encrypt


try:
    import requests
    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('AdminUserController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/getossak', methods=['GET'])
@get_require_check_with_permissions([])
def getossak(user_id, company_id, args):
    d = dict()
    d["BUCKET"] = conf.config["OSS_BUCKET"]
    d["REGION"] = conf.config['OSS_REGION']
    d["ENDPOINT"] = conf.config['OSS_POINT']
    d["OSS_ALL_KEY"] = conf.config['OSS_ALL_KEY']
    d["OSS_ALL_SECRET"] = conf.config['OSS_ALL_SECRET']
    return d


@bp.route('/me', methods=['GET'])
@get_require_check_with_permissions([])
def login_user_info(user_id, company_id, args):
    return AdminUserService.login_user_info(user_id)


@bp.route('/adminuser/list', methods=['GET'])
@get_require_check_with_permissions([])
def admin_user_list(user_id, company_id, args):
    """
PC端用户列表
PC端用户列表，需要先登录
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
  - name: limit
    in: query
    type: integer
    required: true
  - name: username
    in: query
    type: string
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
              pk:
                type: integer
                description: id
              date_joined:
                type: string
                description: 注册时间
              is_active:
                type: string
                description: 是否激活
              mobile:
                type: string
                description: 手机号
              nickname:
                type: string
                description: 昵称
              show_name:
                type: string
                description: 角色显示昵称
              username:
                type: string
                description: 用户名
              company_name:
                type: string
                description: 公司名字
    """
    offset = int(args['offset'])
    limit = int(args['limit'])
    username = args.get('username', None)
    return AdminUserService.admin_user_list(company_id, offset, limit, username)


@bp.route('/adminuser/change/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def admin_user_update(user_id, company_id, args, pk):
    """

修改PC端用户
修改PC端用户，需要先登录
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
        is_active:
          type: string
          description: 是否激活
        password:
          type: string
          description: 密码
        nickname:
          type: string
          description: 昵称
        permissions:
          type: string
          description: 权限数组 [{"permission_id":1,"permission_name":"增加广告","group":"广告"}]
        role:
          type: integer
          description: 角色id
        username:
          type: string
          description: 用户名
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
    password = args.get('password', None)
    is_active = args.get('is_active', None)
    permissions = args.get('permissions', None)
    role = args.get('role', None)
    username = args.get('username', None)
    nickname = args.get('nickname', None)
    ret = AdminUserService.admin_user_update(
        company_id, pk, is_active, permissions,
        role, username, password, nickname)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.ADMIN_USER_PERMISSION_GT_COMPANY)
    return ret


@bp.route('/adminuser/add', methods=['POST'])
@post_require_check_with_permissions([])
def admin_user_add_api(user_id, company_id, args):
    """

添加PC端用户
添加PC端用户，需要先登录
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
        is_active:
          type: string
          description: 是否激活
        mobile:
          type: string
          description: 手机号
        nickname:
          type: string
          description: 昵称
        permissions:
          type: string
          description: 权限数组 [{"permission_id":1,"permission_name":"增加广告","group":"广告"}]
        role:
          type: integer
          description: 角色id
        username:
          type: string
          description: 用户名
        password:
          type: string
          description: 密码
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
    is_active = args.get('is_active')
    mobile = args.get('mobile')
    nickname = args.get('mobile')
    permissions = args.get('permissions')
    role = args.get('role')
    username = args.get('username')
    password = args['password']
    ret = AdminUserService.admin_user_add(
        company_id, password, username, permissions, role)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret


@bp.route('/adminuser/retrieve/<int:pk>', methods=['GET'])
@get_require_check_with_permissions([])
def admin_user_retrieve(user_id, company_id, args, pk):
    """
检索PC端用户
检索PC端用户，需要先登录
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
              pk:
                type: integer
                description: id
              company_id:
                type: integer
                description: 公司id
              role:
                type: integer
                description: 角色id
              date_joined:
                type: string
                description: 注册时间
              is_active:
                type: string
                description: 是否激活
              mobile:
                type: string
                description: 手机号
              nickname:
                type: string
                description: 昵称
              permissions:
                type: array
                items:
                  properties:
                    permission_name:
                      type: string
                      description: 权限名字
                    permission_id:
                      type: integer
                      description: 权限id
                    group:
                      type: string
                      description: 组
    """
    return AdminUserService.admin_user_retrieve(pk)


@bp.route('/adminuser/disable/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def admin_user_disable(user_id, company_id, args, pk):
    """

禁用PC端用户
禁用PC端用户，需要先登录
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
    description: 用户pk
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

    ret = AdminUserService.admin_user_disable_enable(pk, 0)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret


@bp.route('/adminuser/enable/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def admin_user_enable_api(user_id, company_id, args, pk):
    """

启用PC端用户
启用PC端用户，需要先登录
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
    description: 用户pk
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

    ret = AdminUserService.admin_user_disable_enable(pk, 1)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret


@bp.route('/adminuser/pwd/change', methods=['POST'])
@post_require_check_with_permissions([])
def admin_user_pwd_change_api(user_id, company_id, args):
    """
修改密码
修改密码，需要先登录
---
tags:
  - 后台管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
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
    old_password = args['old_password']
    new_password = args['new_password']
    ret = AdminUserService.change_pwd(user_id, old_password, new_password)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.ADMIN_USER_PWD_ERROR)
    return ret


@bp.route('/login', methods=['POST'])
@post_require_check(['username', 'password'])
def user_login(args):
    """
    用户登录
    登录
    ---
    tags:
      - 用户模块
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: 用户名字
            password:
              type: string
              description: 密码
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
                token:
                  type: string
                  description: token串,登录的时候放到header
                user:
                  type: object
                  properties:
                    id:
                      type: integer
                      description: 用户id
                    username:
                      type: string
                      description: 用户名字

    """
    username = args['username']
    password = args['password']

    if username == '' or password == '':
        raise AppError(*SubErrorCode.USER_PWD_ERR)

    user_obj = AdminUserService.get_user_by_username(username)
    if user_obj == -1:
        raise AppError(*SubErrorCode.USER_PWD_ERR)

    if user_obj == -2:
        raise AppError(*SubErrorCode.APP_USER_DISABLED)

    password_md5_str = md5_encrypt(password)
    if user_obj["password"] != password_md5_str:
        raise AppError(*SubErrorCode.USER_PWD_ERR)

    token = gen_token(password, conf.config["SALT"], 3600)
    AdminUserService.login(user_obj["id"], token)

    return {
        'token': token,
        'user': {
            'id': user_obj['id'],
            'username': user_obj['username']
        }
    }
