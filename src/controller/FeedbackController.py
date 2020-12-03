# coding:utf-8
try:
    from flask.blueprints import Blueprint
    from core.framework import get_require_check_with_permissions, \
        post_require_check_with_permissions
    from core.AppError import AppError
    from utils.defines import GlobalErrorCode, SubErrorCode
    from service.FeedbackService import FeedbackService

except:
    import traceback
    print traceback.format_exc()

try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('FeedbackController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/feedback/list', methods=['GET'])
@get_require_check_with_permissions([])
def feedback_list_api(user_id, company_id, args):
    """
反馈列表
反馈列表，需要先登录
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
    return FeedbackService.feedback_list(company_id, offset, limit)


@bp.route('/feedback/change/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def feedback_change_api(user_id, company_id, args, pk):
    """
处理反馈
处理反馈，需要先登录
---
tags:
  - 运营管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: PK
    in: path
    type: integer
    description: PK
  - name: body
    in: body
    required: true
    schema:
      properties:
        remarks:
          type: string
          description: 备注

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
    remarks = args['remarks']
    return FeedbackService.feedback_change(pk, remarks)

