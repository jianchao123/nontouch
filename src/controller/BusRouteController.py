# coding:utf-8

from flask.blueprints import Blueprint

from core.framework import get_require_check_with_permissions, \
    post_require_check_with_permissions
from core.AppError import AppError
from utils.defines import SubErrorCode, GlobalErrorCode

from service.RouteService import BusRouteService


try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('BusRouteController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/route/list', methods=['GET'])
@get_require_check_with_permissions([])
def route_list(user_id, company_id, args):
    """
线路列表
线路列表，需要先登录
---
tags:
  - 商家管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: line_no
    in: query
    type: string
    description: 线路名字
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
              company:
                type: integer
                description: 公司id
              company_name:
                type: string
                description: 公司名字
              end_time:
                type: string
                description: 末班时间
              start_time:
                type: string
                description: 首班时间
              fees:
                type: number
                description: 线路乘车费用
              line_no:
                type: string
                description: 线路名字
              status:
                type: integer
                description: 1启用 2禁用
    """
    line_no = args.get('line_no', None)
    offset = args.get('offset')
    limit = args.get('limit')
    ret = BusRouteService.route_list(company_id, line_no, offset, limit)
    if type(ret) == int and ret == -1:
        raise AppError(*SubErrorCode.NOT_PC_USER)
    return ret


@bp.route('/route/add', methods=['POST'])
@post_require_check_with_permissions([])
def route_add(user_id, company_id, args):
    """
添加线路
添加线路，需要先登录
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
        start_time:
          type: string
          description: 首班时间
        end_time:
          type: string
          description: 末班时间
        fees:
          type: number
          description: 乘车费用
        line_no:
          type: string
          description: 线路名字
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
              description: 新增的线路Id
    """
    start_time = args['start_time']
    end_time = args['end_time']
    fees = args['fees']
    line_no = args['line_no']
    try:
        int(line_no)
    except:
        raise AppError(*SubErrorCode.ROUTE_NAME_ONLY_NUMBERS)
    ret = BusRouteService.route_add(
        company_id, start_time, end_time, fees, line_no)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret


@bp.route('/route/change/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def route_update(user_id, company_id, args, pk):
    """
更新线路
更新线路，需要先登录
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
    description: 线路pk
  - name: body
    in: body
    required: true
    schema:
      properties:
        start_time:
          type: string
          description: 首班时间
        end_time:
          type: string
          description: 末班时间
        fees:
          type: number
          description: 乘车费用
        line_no:
          type: string
          description: 线路名字
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
              description: 新增的线路Id
    """
    start_time = args['start_time']
    end_time = args['end_time']
    fees = args['fees']
    line_no = args['line_no']
    ret = BusRouteService.route_update(pk, start_time, end_time, fees, line_no)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret


@bp.route('/route/disable/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def route_disable(user_id, company_id, args, pk):
    """

禁用线路
禁用线路，需要先登录
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
    description: 线路pk

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
    ret = BusRouteService.route_disable(pk)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -3:
        raise AppError(*SubErrorCode.STATUS_ERR)
    return ret


@bp.route('/route/enable/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def route_enable(user_id, company_id, args, pk):
    """

启用线路
启用线路，需要先登录
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
    description: 线路pk

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
    ret = BusRouteService.route_enable(pk)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -3:
        raise AppError(*SubErrorCode.STATUS_ERR)
    return ret