# coding:utf-8

from flask.blueprints import Blueprint

from core.framework import get_require_check_with_permissions, \
    post_require_check_with_permissions
from core.AppError import AppError
from utils.defines import SubErrorCode, GlobalErrorCode

from service.CarService import CarService

try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('CarController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/car/list', methods=['GET'])
@get_require_check_with_permissions([])
def car_list(user_id, company_id, args):
    """
车辆列表
车辆列表，需要先登录
---
tags:
  - 商家管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: not_binding
    in: query
    type: integer
    description: 是否查询未绑定设备的的车辆
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
              bus_id:
                type: string
                description: 车牌号
              brand:
                type: string
                description: 品牌
              type:
                type: string
                description: 类型
              model_number:
                type: string
                description: 型号
              engine:
                type: string
                description: 引擎
              chassis:
                type: string
                description: 底盘
              load:
                type: string
                description: 载重
              bus_load:
                type: string
                description: 载客量
              product_date:
                type: string
                description: 生产日期
              buy_date:
                type: string
                description: 购买日期
              status:
                type: integer
                description: 状态 1未绑线 2已绑线 10删除
              company_id:
                type: integer
                description: 公司id
              company_name:
                type: string
                description: 公司名字
              line_no:
                type: string
                description: 线路名字
              is_servicing:
                type: integer
                description: 是否运营中 1是 0否

    """
    offset = args['offset']
    limit = args['limit']
    bus_id = args.get('bus_id', None)
    not_binding = args.get('not_binding', None)
    return CarService.car_list(company_id, bus_id, not_binding, offset, limit)


@bp.route('/car/change/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def car_update(user_id, company_id, args, pk):
    """

修改车辆
修改车辆，需要先登录
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
    description: 车辆pk
  - name: body
    in: body
    required: true
    schema:
      properties:
        bus_id:
          type: string
          description: 车牌号
        brand:
          type: string
          description: 品牌
        type:
          type: string
          description: 类型
        model_number:
          type: string
          description: 型号
        engine:
          type: string
          description: 引擎
        chassis:
          type: string
          description: 底盘
        load:
          type: string
          description: 载重
        bus_load:
          type: string
          description: 载客量
        product_date:
          type: string
          description: 生产日期
        buy_date:
          type: string
          description: 购买日期
        is_servicing:
          type: integer
          description: 是否营运中 1是 2否
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
    bus_id = args.get('bus_id', None)
    bus_load = args.get('bus_load', None)
    buy_date = args.get('buy_date', None)
    chassis = args.get('chassis', None)
    engine = args.get('engine', None)
    load = args.get('load', None)
    model_number = args.get('model_number', None)
    product_date = args.get('product_date', None)
    type = args.get('type', None)
    is_servicing = args.get('is_servicing', None)

    ret = CarService.car_update(pk, brand, bus_id, bus_load,
                                buy_date, chassis, engine, load,
                                model_number, product_date,
                                type, is_servicing)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret


@bp.route('/car/add', methods=['POST'])
@post_require_check_with_permissions([])
def car_add(user_id, company_id, args):
    """

添加车辆
添加车辆，需要先登录
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
        bus_id:
          type: string
          description: 车牌号
        brand:
          type: string
          description: 品牌
        type:
          type: string
          description: 类型
        model_number:
          type: string
          description: 型号
        engine:
          type: string
          description: 引擎
        chassis:
          type: string
          description: 底盘
        load:
          type: string
          description: 载重
        bus_load:
          type: string
          description: 载客量
        product_date:
          type: string
          description: 生产日期
        buy_date:
          type: string
          description: 购买日期
        is_servicing:
          type: integer
          description: 是否营运中 1是 2否
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
    brand = args['brand']
    bus_id = args['bus_id']
    bus_load = int(args['bus_load'])
    buy_date = args['buy_date']
    chassis = args['chassis']
    engine = args['engine']
    load = args.get('load', None)
    model_number = args['model_number']
    product_date = args['product_date']
    type = args['type']
    is_servicing = int(args['is_servicing'])
    ret = CarService.car_add(company_id, brand, bus_id, bus_load, buy_date,
                             chassis, engine, load, model_number, product_date,
                             type, is_servicing)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)


@bp.route('/car/binding/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def car_binding(user_id, company_id, args, pk):
    """
车辆绑定线路
车辆绑定线路，需要先登录
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
    description: 车辆pk
  - name: body
    in: body
    required: true
    schema:
      properties:
        route_id:
          type: string
          description: 线路id

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
    route_id = args['route_id']
    ret = CarService.car_binding(pk, route_id)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -3:
        raise AppError(*SubErrorCode.STATUS_ERR)
    if ret == -4:
        raise AppError(*SubErrorCode.ROUTE_ALREADY_DISABLED)
    return ret


@bp.route('/car/unbinding/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def device_unbinding(user_id, company_id, args, pk):
    """
车辆解除绑定线路
车辆解除绑定线路，需要先登录
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
    description: 车辆pk

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
    ret = CarService.car_unbinding(pk)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -3:
        raise AppError(*SubErrorCode.STATUS_ERR)
    return ret
