# coding:utf-8

from flask.blueprints import Blueprint
from core.framework import get_require_check_with_permissions, \
    post_require_check_with_permissions
from core.AppError import AppError
from utils.defines import GlobalErrorCode, SubErrorCode

from service.NoticeService import NoticeService

try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('NoticeController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/notice/list', methods=['GET'])
@get_require_check_with_permissions([])
def notice_list(user_id, company_id, args):
    """
公告列表
公告列表，需要先登录
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
    return NoticeService.notice_list(company_id, offset, limit)


@bp.route('/notice/add', methods=['POST'])
@post_require_check_with_permissions([])
def notice_add(user_id, company_id, args):
    """
公告列表
公告列表，需要先登录
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
        name:
          type: string
          description: 公告名字
        content:
          type: string
          description: 内容
        start_time:
          type: string
          description: 开始时间
        end_time:
          type: string
          description: 结束时间
        priorty:
          type: integer
          description: 优先级
        is_active:
          type: integer
          description: 是否上线
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
    name = args['name']
    content = args['content']
    start_time = args['start_time']
    return NoticeService.notice_add(company_id, name, content, start_time)


@bp.route('/notice/change/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def notice_change(user_id, company_id, args, pk):
    """
公告修改
公告修改，需要先登录
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
        name:
          type: string
          description: 公告名字
        content:
          type: string
          description: 内容
        start_time:
          type: string
          description: 开始时间
        end_time:
          type: string
          description: 结束时间
        is_active:
          type: integer
          description: 是否上线
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
    name = args['name']
    content = args['content']
    start_time = args['start_time']
    return NoticeService.notice_change(
        pk, name, content, start_time)


@bp.route('/notice/delete/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def notice_delete(user_id, company_id, args, pk):
    """
删除公告
删除公告，需要先登录
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
    return NoticeService.notice_delete(pk)


@bp.route('/notice/online/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def notice_online(user_id, company_id, args, pk):
    """
公告上线
公告上线，需要先登录
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
    return NoticeService.notice_offline_online(pk, 1)


@bp.route('/notice/offline/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def notice_offline(user_id, company_id, args, pk):
    """
公告下线
公告下线，需要先登录
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
    return NoticeService.notice_offline_online(pk, 0)
