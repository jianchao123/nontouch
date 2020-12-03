# coding:utf-8
try:
    from flask.blueprints import Blueprint
    from core.framework import get_require_check_with_permissions, \
        post_require_check_with_permissions
    from core.AppError import AppError
    from utils.defines import GlobalErrorCode, SubErrorCode

    from service.LostAndFoundService import LostAndFoundService
except:
    import traceback
    print traceback.format_exc()
try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('LostAndFoundController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/lostandfound/list', methods=['GET'])
@get_require_check_with_permissions([])
def lostandfound_list(user_id, company_id, args):
    """
失物招领列表
失物招领列表，需要先登录
---
tags:
  - 运营管理
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
        offset:
          type: integer
          description: OFFSET
        limit:
          type: integer
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
          type: object
          properties:
            id:
              type: integer
              description: pk
    """
    offset = int(args['offset'])
    limit = int(args['limit'])
    return LostAndFoundService.lostandfound_list(company_id, offset, limit)


@bp.route('/lostandfound/add', methods=['POST'])
@post_require_check_with_permissions([])
def lostandfound_add(user_id, company_id, args):
    """
失物招领列表
失物招领列表，需要先登录
---
tags:
  - 运营管理
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
        description:
          type: string
          description: 描述
        city:
          type: string
          description: 城市
        line_no:
          type: string
          description: 线路
        contacts:
          type: string
          description: 联系方式
        imgs:
          type: integer
          description: 图片
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
    description = args['description']
    city = args['city']
    line_no = args['line_no']
    contacts = args['contacts']
    imgs = args['imgs']
    ret = LostAndFoundService.lostandfound_add(
        company_id, user_id, description, city, line_no, contacts, imgs)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)


@bp.route('/lostandfound/change/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def lostandfound_change(user_id, company_id, args, pk):
    """
失物招领修改
失物招领修改，需要先登录
---
tags:
  - 运营管理
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
    description: PK
  - name: body
    in: body
    required: true
    schema:
      properties:
        description:
          type: string
          description: 描述
        city:
          type: string
          description: 城市
        line_no:
          type: string
          description: 线路
        contacts:
          type: string
          description: 联系方式
        imgs:
          type: integer
          description: 图片
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
    description = args['description']
    city = args['city']
    line_no = args['line_no']
    contacts = args['contacts']
    imgs = args['imgs']
    return LostAndFoundService.lostandfound_change(
        pk, description, city, line_no, contacts, imgs)


@bp.route('/lostandfound/delete/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def lostandfound_delete(user_id, company_id, args, pk):
    """
删除失物招领
删除失物招领，需要先登录
---
tags:
  - 运营管理
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
    description: PK

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
    return LostAndFoundService.lostandfound_delete(pk)
