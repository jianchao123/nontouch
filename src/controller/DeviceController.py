# coding:utf-8

from flask.blueprints import Blueprint
from core.framework import get_require_check_with_permissions, \
    post_require_check_with_permissions
from core.AppError import AppError
from utils.defines import SubErrorCode, GlobalErrorCode
from service.DeviceService import DeviceService

try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('DeviceController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/device/list', methods=['GET'])
@get_require_check_with_permissions([])
def device_list(user_id, company_id, args):
    """
设备列表
设备列表，需要先登录
---
tags:
  - 商家管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: device_no
    in: query
    type: string
    description: 设备号
  - name: bus_id
    in: query
    type: string
    description: 车牌号
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
              brand:
                type: string
                description: 品牌
              buy_date:
                type: string
                description: 购买时间
              car:
                type: integer
                description: 绑定的车辆id
              device_no:
                type: string
                description: 设备号
              is_binding:
                type: integer
                description: 是否绑定
              manufacture_date:
                type: string
                description: 生产日期
              model_number:
                type: integer
                description: 型号
              name:
                type: string
                description: 设备名称
              pro_seq_number:
                type: string
                description: 生产序号
              status:
                type: integer
                description: 状态 1未分配 2已分配,未绑车 3已绑车 10删除
    """
    device_no = args.get('device_no', None)
    car_no = args.get('bus_id', None)
    offset = args['offset']
    limit = args['limit']
    return DeviceService.device_list(company_id, car_no, device_no, offset, limit)


@bp.route('/device/change/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def device_update(user_id, company_id, args, pk):
    """

修改设备
修改设备，需要先登录
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
    description: 设备pk
  - name: body
    in: body
    required: true
    schema:
      properties:
        name:
          type: string
          description: 设备名称
        brand:
          type: string
          description: 设备品牌
        type:
          type: integer
          description: 设备类型 1扫码设备 2人脸设备 3刷卡 4刷卡扫码二合一
        model_number:
          type: string
          description: 型号
        pro_seq_number:
          type: string
          description: 生产序号
        device_no:
          type: string
          description: 设备号
        manufacture_date:
          type: string
          description: 生产时间
        buy_date:
          type: string
          description: 购买时间
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
    brand = args.get('brand', None)
    buy_date = args.get('buy_date', None)
    device_no = args.get('device_no', None)
    manufacture_date = args.get('manufacture_date', None)
    model_number = args.get('model_number', None)
    name = args.get('name', None)
    pro_seq_number = args.get('pro_seq_number', None)
    type = args.get('type', None)
    ret = DeviceService.device_update(
        pk, brand, buy_date, device_no, manufacture_date,
        model_number, name, pro_seq_number, type)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return {'id': ret}


@bp.route('/device/add', methods=['POST'])
@post_require_check_with_permissions([])
def device_add(user_id, company_id, args):
    """
添加设备
添加设备，需要先登录
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
    description: 设备pk
  - name: body
    in: body
    required: true
    schema:
      properties:
        name:
          type: string
          description: 设备名称
        brand:
          type: string
          description: 设备品牌
        type:
          type: integer
          description: 设备类型 1扫码设备 2人脸设备 3刷卡 4刷卡扫码二合一
        model_number:
          type: string
          description: 型号
        pro_seq_number:
          type: string
          description: 生产序号
        device_no:
          type: string
          description: 设备号
        manufacture_date:
          type: string
          description: 生产时间
        buy_date:
          type: string
          description: 购买时间
        company_id:
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
              description: 修改成功的Id
    """
    brand = args.get('brand')
    buy_date = args.get('buy_date')
    device_no = args.get('device_no')
    manufacture_date = args.get('manufacture_date')
    model_number = args.get('model_number')
    name = args.get('name')
    pro_seq_number = args.get('pro_seq_number')
    type = args.get('type')
    ret = DeviceService.device_add(company_id, brand, buy_date, device_no,
                                   manufacture_date, model_number, name,
                                   pro_seq_number, type)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return {'id': ret}


@bp.route('/device/binding/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def device_binding(user_id, company_id, args, pk):
    """
    设备绑定车辆
设备绑定车辆，需要先登录
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
    description: 设备pk
  - name: body
    in: body
    required: true
    schema:
      properties:
        car_id:
          type: integer
          description: 车辆id

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
              description: 绑定成功的Id
    """
    car_id = args['car_id']
    ret = DeviceService.binding_car(car_id, pk)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -3:
        raise AppError(*SubErrorCode.STATUS_ERR)
    if ret == -4:
        raise AppError(*SubErrorCode.NOT_PC_USER)
    return {}


@bp.route('/device/unbinding/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def device_unbinding(user_id, company_id, args, pk):
    """
设备解除绑定车辆
设备解除绑定车辆，需要先登录
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
    description: 设备pk

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
              description: 解除绑定成功的Id
    """
    ret = DeviceService.unbinding_car(pk)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -3:
        raise AppError(*SubErrorCode.STATUS_ERR)
    if ret == -4:
        raise AppError(*SubErrorCode.NOT_PC_USER)
    return {}
