# coding:utf-8
try:
    from flask.blueprints import Blueprint

    from core.framework import get_require_check_with_permissions, \
        post_require_check_with_permissions
    from core.AppError import AppError
    from utils.defines import SubErrorCode, GlobalErrorCode

    from service.CertificationService import CertificationService
except:
    import traceback
    print traceback.format_exc()
try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('CertificationController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/certification/list', methods=['GET'])
@get_require_check_with_permissions([])
def certification_list_api(user_id, company_id, args):
    """
审核列表
审核列表，需要先登录
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
        status:
          type: integer
          description: 状态 1审核中 2审核通过 3审核失败
        identity_id:
          type: integer
          description: 身份Id
        mobile:
          type: string
          description: 手机号

responses:
  200:
    description: 正常返回http code 200
    schema:
      properties:
        detail:
          type: string
          description: 错误消息
        code:
          type: integer
          description: 状态
        data:
          type: object
          properties:
            id:
              type: string
              description: PK

    """
    status = args.get('status', None)
    identity_id = args.get('identity_id', None)
    offset = args['offset']
    limit = args['limit']
    mobile = args['mobile']
    return CertificationService.certification_list(
        company_id, mobile, status, identity_id, offset, limit)


@bp.route('/certification/audit/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def certification_audit_api(user_id, company_id, args, pk):
    """
审核
审核，需要先登录
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
        status:
          type: integer
          description: 状态 1审核中 2审核通过 3审核失败
        pass_reason:
          type: string
          description: 通过原因
        end_time:
          type: string
          description: 结束时间
        discount_rate:
          type: string
          description: 折扣比率 例 0.02

responses:
  200:
    description: 正常返回http code 200
    schema:
      properties:
        detail:
          type: string
          description: 错误消息
        code:
          type: integer
          description: 状态
        data:
          type: object
          properties:
            id:
              type: string
              description: PK
    """
    status = int(args['status'])
    pass_reason = str(args['pass_reason'])
    end_time = args['end_time']
    discount_rate = args['discount_rate']
    ret = CertificationService.audit(
        pk, user_id, status, pass_reason, end_time, discount_rate)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.STATUS_ERR)
    return ret


