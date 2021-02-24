# coding:utf-8

from flask.blueprints import Blueprint
from core.framework import get_require_check_with_permissions
from service.DistrictCodeService import DistrictCodeService


try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('DistrictController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/districtcode/list', methods=['GET'])
@get_require_check_with_permissions([])
def districtcode_list(user_id, company_id, args):
    """
区域代码
区域代码，需要先登录
---
tags:
  - APP
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
          description: 状态
        data:
          type: array
          items:
            properties:
              id:
                type: string
                description: 区域代码
              pk:
                type: integer
                description: 主键
              name:
                type: string
                description: 区域名称
              city:
                type: array
                items:
                  properties:
                    id:
                      type: string
                      description: 区域代码
                    pk:
                      type: integer
                      description: 主键
                    name:
                      type: string
                      description: 区域名称
                    county:
                      type: array
                      items:
                        properties:
                          id:
                            type: string
                            description: 区域代码
                          pk:
                            type: integer
                            description: 主键
                          name:
                            type: string
                            description: 区域名称

    """
    return DistrictCodeService.district_code_list()