# coding:utf-8
try:
    from flask.blueprints import Blueprint
    from core.framework import get_require_check_with_permissions, \
        post_require_check_with_permissions
except:
    import traceback
    print traceback.format_exc()

from service.AdvertService import AdvertService

try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('AdvertController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/advert/list', methods=['GET'])
@get_require_check_with_permissions([])
def advert_list(user_id, company_id, args):
    """
广告列表
广告列表，需要先登录
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
    return AdvertService.advert_list(company_id, offset, limit)


@bp.route('/advert/add', methods=['POST'])
@post_require_check_with_permissions([])
def advert_add(user_id, company_id, args):
    """
广告列表
广告列表，需要先登录
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
          description: 广告名字
        image:
          type: string
          description: 图片
        start_time:
          type: string
          description: 开始时间
        end_time:
          type: string
          description: 结束时间
        url:
          type: string
          description: 广告链接
        is_active:
          type: integer
          description: 是否上线
        adv_location:
          type: integer
          description: 展示位置 1首页 2弹出框 3首次开启

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
    image = args['image']
    start_time = args['start_time']
    end_time = args['end_time']
    url = args['url']
    is_active = args['is_active']
    adv_location = args['adv_location']
    return AdvertService.advert_add(company_id, name, image, url, start_time,
                                    end_time, is_active, adv_location)


@bp.route('/advert/change/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def advert_change(user_id, company_id, args, pk):
    """
广告修改
广告修改，需要先登录
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
          description: 广告名字
        image:
          type: string
          description: 图片
        start_time:
          type: string
          description: 开始时间
        end_time:
          type: string
          description: 结束时间
        url:
          type: string
          description: 广告链接
        is_active:
          type: integer
          description: 是否上线
        adv_location:
          type: integer
          description: 展示位置 1首页 2弹出框 3首次开启
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
    image = args['image']
    start_time = args['start_time']
    end_time = args['end_time']
    url = args['url']
    is_active = args['is_active']
    adv_location = args['adv_location']
    return AdvertService.advert_change(pk, name, image, url, start_time,
                                       end_time, is_active, adv_location)


@bp.route('/advert/delete/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def advert_delete(user_id, company_id, args, pk):
    """
删除广告
删除广告，需要先登录
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
    return AdvertService.advert_delete(pk)


@bp.route('/advert/online/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def advert_online(user_id, company_id, args, pk):
    """
广告上线
广告上线，需要先登录
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
    return AdvertService.advert_offline_online(pk, 1)


@bp.route('/advert/offline/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def advert_offline(user_id, company_id, args, pk):
    """
广告下线
广告下线，需要先登录
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
    return AdvertService.advert_offline_online(pk, 0)
