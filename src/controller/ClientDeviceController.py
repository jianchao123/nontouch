# coding:utf-8

from flask.blueprints import Blueprint
from core.framework_1 import post_require_check, get_require_check
from core.AppError import AppError
from utils.defines import GlobalErrorCode, SubErrorCode
from service.ClientDeviceService import ClientDeviceService


try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('ClientDeviceController', __name__)
"""蓝图url前缀"""
url_prefix = '/api/v1'


@bp.route('/face-access_token/', methods=['GET'])
@get_require_check([])
def get_baidu_access_token(args):
    """
 获取百度访问token
获取百度访问token
---
tags:
  - 机具
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
          description: 状态 200096 获取token错误
        data:
          type: object
          properties:
            access_token:
              type: string
              description: 访问token
    """
    ret = ClientDeviceService.get_baidu_access_token()
    if ret == -1:
        raise AppError(*SubErrorCode.DEVICE_GET_TOKEN_ERROR)
    return ret


@bp.route('/get_device_info/', methods=['GET'])
@get_require_check(['device_no'])
def get_device_info(args):
    """
获取设备信息
获取设备信息
---
tags:
  - 机具
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
          description: 状态 200096 获取token错误
        data:
          type: object
          properties:
            fees:
              type: number
              description: 乘车金额
    """
    device_no = args['device_no']
    ret = ClientDeviceService.get_device_info(device_no)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -10:
        raise AppError(*SubErrorCode.DEVICE_NOT_BINDING)
    if ret == -11:
        raise AppError(*SubErrorCode.CAR_NOT_BINDING_ROUTE)
    return ret


@bp.route('/deviceupdatestrategy/', methods=['POST'])
@post_require_check(['device_no', 'mobiles'])
def device_update_strategy(args):
    """
设备更新策略数据
设备更新策略数据
---
tags:
  - 机具
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
        device_no:
          type: string
          description: 设备号
        mobiles:
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
          description: 状态 200096 获取token错误
        data:
          type: object
          properties:
            add:
              type: array
              items:
                properties:
                  mobile:
                    type: string
                    description: 手机号
                  oss_url:
                    type: string
                    description: oss url
            upgrade:
              type: array
              items:
                properties:
                  mobile:
                    type: string
                    description: 手机号
                  oss_url:
                    type: string
                    description: oss url
            delete:
              type: array
              items:
                mobile:
                  type: string
    """
    device_no = args['device_no']
    data = args['data']
    ret = ClientDeviceService.device_update_strategy(device_no, data)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -10:
        raise AppError(*SubErrorCode.DEVICE_NOT_BINDING)
    if ret == -11:
        raise AppError(*SubErrorCode.CAR_NOT_BINDING_ROUTE)
    return ret