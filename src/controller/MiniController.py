# coding:utf-8
try:
    from flask.blueprints import Blueprint
    from core.framework_1 import get_require_check, post_require_check
    from core.AppError import AppError
    from utils.defines import GlobalErrorCode, SubErrorCode
    from service.MiniService import MiniService
    from ext import conf
except:
    import traceback
    print traceback.format_exc()

try:
    import requests
    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('MiniController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/getloginstatus/', methods=['GET'])
@get_require_check([])
def mini_get_login_status(args):
    """
小程序获取登录状态
小程序获取登录状态
---
tags:
  - 小程序
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
        code:
          type: string
          description: session code

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
          description: 状态 200230 小程序解析code失败
        data:
          type: object
          properties:
            is_new_user:
              type: integer
              description: 是否新用户
            token:
              type: string
              description: 新生成的token
    """
    code = args['code']
    ret = MiniService.get_login_status(code)
    if ret == -10:
        raise AppError(*SubErrorCode.MINI_DECRYPT_FAIL)
    return ret


@bp.route('/signupuser/', methods=['GET'])
@get_require_check([])
def mini_sign_up_user(args):
    """
小程序获取登录状态
小程序获取登录状态
---
tags:
  - 小程序
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
        encryptedData:
          type: string
          description: 加密数据
        iv:
          type: string
          description: IV

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
          description: 状态 200230 小程序解析code失败
        data:
          type: object
          properties:
            phone:
              type: string
              description: 手机号

    """
    from flask import request
    token = request.headers.get('token')
    encrypted_data = args['encryptedData']
    iv = args['iv']
    print token, encrypted_data, iv
    ret = MiniService.sign_up_user(encrypted_data, iv, token)
    if ret == -10:
        raise AppError(*GlobalErrorCode.PARAM_ERROR)
    if ret == -11:
        raise AppError(*SubErrorCode.MINI_DECRYPT_FAIL)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret


@bp.route('/uploadtobaidu/', methods=['POST'])
@post_require_check([])
def mini_upload_to_baidu(args):
    """
小程序上传人脸到百度人脸库
小程序上传人脸到百度人脸库
---
tags:
  - 小程序
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
        url:
          type: string
          description: 图片oss链接
        mobile:
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
          description: 状态 200230 小程序解析code失败
        data:
          type: object
          properties:
            id:
              type: integer
              description: face id

    """
    url = args['url']
    mobile = args['mobile']
    ret = MiniService.upload_baidu(url, mobile)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.FACE_UPLOAD_IMAGE_NOT_FACE)
    return ret
#
#
# @bp.route('/uploadtooss/', methods=['POST'])
# @post_require_check([])
# def mini_upload_to_oss(args):
#     """
# 小程序上传人脸到oss
# 小程序上传人脸到oss
# ---
# tags:
#   - 小程序
# parameters:
#   - name: token
#     in: header
#     type: string
#     required: true
#     description: TOKEN
#   - name: body
#     in: body
#     required: true
#     schema:
#       properties:
#         image:
#           type: string
#           description: 图片bytes
#
# responses:
#   200:
#     description: 正常返回http code 200
#     schema:
#       properties:
#         msg:
#           type: string
#           description: 错误消息
#         status:
#           type: integer
#           description: 状态 200230 小程序解析code失败
#         data:
#           type: object
#           properties:
#             path:
#               type: string
#               description: 小程序使用的路径
#
#     """
#     image = args['image']
#     return MiniService.upload_oss(image)
