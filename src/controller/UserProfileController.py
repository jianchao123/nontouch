# coding:utf-8
try:
    from flask.blueprints import Blueprint
    from core.framework import post_require_check, \
        get_require_check_with_permissions, post_require_check_with_permissions
    from core.AppError import AppError
    from utils.defines import SubErrorCode, GlobalErrorCode
    from ext import conf

    from service.UserProfileService import UserProfileService
except:
    import traceback
    print traceback.format_exc()


try:
    import requests
    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('UserProfileController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/mysql_user/list', methods=['GET'])
@get_require_check_with_permissions([])
def app_user_list(user_id, company_id, args):
    """
    APP用户列表
    APP用户列表，需要先登录
    ---
    tags:
      - 用户模块
    parameters:
      - name: token
        in: header
        type: string
        required: true
        description: TOKEN
      - name: mobile
        in: query
        type: string
        required: false
        description: 手机号
      - name: offset
        in: query
        type: integer
        description: offset
      - name: limit
        type: integer
        in: query
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
                  date_joined:
                    type: string
                    description: 注册时间
                  coupons:
                    type: array
                    description: 优惠券
                    items:
                      properties:
                        face_value:
                          type: integer
                          description: 面值
                        code:
                          type: string
                          description: 券码
                  sub_account:
                    type: array
                    description: 子账号
                    items:
                      properties:
                        sub_account_mobile:
                          type: string
                          description: 子帐号
                        sub_account_name:
                          type: string
                          description: 子帐号名字
                        oss_url:
                          type: string
                          description: 人脸url
    """
    mobile = args.get('mobile', None)
    offset = int(args['offset'])
    limit = int(args['limit'])
    ret = UserProfileService.app_user_list(company_id, mobile, offset, limit)
    return ret


@bp.route('/mysql_user/deposit/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def app_user_change(user_id, company_id, args, pk):
    """
    添加余额
    添加余额，需要先登录
    ---
    tags:
      - 用户模块
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
      - name: body
        in: body
        required: true
        schema:
          properties:
            balance:
              type: number
              description: 增加余额

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
    balance = args.get('balance', None)
    ret = UserProfileService.app_user_update(pk, company_id, None, balance)
    if ret and ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret and ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return {}


@bp.route('/mysql_user/disable/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def app_user_disable(user_id, company_id, args, pk):
    """
    禁用APP用户
    禁用APP用户，需要先登录
    ---
    tags:
      - 用户模块
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
    ret = UserProfileService.app_user_update(pk, company_id, 0, None)
    if ret and ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret and ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return {'id': ret}


@bp.route('/mysql_user/enable/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def app_user_enable(user_id, company_id, args, pk):
    """
    启用APP用户
    启用APP用户，需要先登录
    ---
    tags:
      - 用户模块
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
    ret = UserProfileService.app_user_update(pk, company_id, 1, None)
    if ret and ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret and ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return {'id': ret}