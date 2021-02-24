# coding:utf-8

from flask.blueprints import Blueprint

from core.framework import get_require_check_with_permissions, \
    post_require_check_with_permissions
from core.AppError import AppError
from utils.defines import SubErrorCode, GlobalErrorCode
from service.StationService import StationService

try:
    import requests
    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('StationController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/station/list', methods=['GET'])
@get_require_check_with_permissions([])
def station_list(user_id, company_id, args):
    """
站点列表
站点列表，需要先登录
---
tags:
  - 商家管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: page
    in: query
    type: integer
    required: true
    description: 页码
  - name: size
    in: query
    type: integer
    required: true
    description: 长度
  - name: bus_route
    in: query
    type: integer
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
              description: 员工id
            company:
              type: integer
              description: 公司id
            company_name:
              type: string
              description: 公司名字
            latitude:
              type: number
              description: 纬度
            longitude:
              type: number
              description: 经度
            line_no:
              type: string
              description: 线路名字
            status:
              type: integer
              description: 1-启用 2-禁用
            number:
              type: integer
              description: 站点号 1 一号站 2 二号站
    """
    route_id = args.get('bus_route', None)
    return StationService.station_list(company_id, route_id)


@bp.route('/station/add', methods=['POST'])
@post_require_check_with_permissions([])
def station_add(user_id, company_id, args):
    """
添加站点
添加站点，需要先登录
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
        data:
          type: string
          description: 例 1,2,3,4  站点id,逗号拼接,按照页面展示顺序拼接
        bus_route:
          type: integer
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
              description: 添加成功返回1


    """
    data = args['data']
    bus_route = args['bus_route']
    ret = StationService.station_add(company_id, data, bus_route)
    if ret == -1:
        raise AppError(*SubErrorCode.NOT_PC_USER)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret

