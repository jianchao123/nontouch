# coding:utf-8

from flask.blueprints import Blueprint

from core.framework import get_require_check_with_permissions, \
    post_require_check_with_permissions
from core.AppError import AppError
from service.CouponTypeService import CouponTypeService
from utils.defines import SubErrorCode, GlobalErrorCode


try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('CouponTypeController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/coupon_type/list', methods=['GET'])
@get_require_check_with_permissions([])
def coupon_type_list(user_id, company_id, args):
    """
活动列表
活动列表，需要先登录
---
tags:
  - 运营管理
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: offset
    in: query
    type: integer
    required: true
    description: OFFSET
  - name: limit
    in: query
    type: integer
    required: true
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
          type: array
          items:
            properties:
              id:
                type: integer
                description: id
              condition:
                type: integer
                description: 活动领取条件 1全部用户 2新注册用户 3分享送券
              content:
                type: string
                description: 内容
              face_value:
                type: number
                description: 面值
              give_out_begin_time:
                type: string
                description: 分发开始时间
              give_out_end_time:
                type: string
                description: 分发结束时间
              img_url:
                type: string
                description: 活动图片
              is_online:
                type: integer
                description: 是否在线
              link:
                type: string
                description: 活动链接
              name:
                type: string
                description: 活动名字
              residue_volume:
                type: integer
                description: 余量
              status:
                type: integer
                description: 状态 1未开始 2活动中 3活动结束 10删除
              type:
                type: integer
                description: 1抵扣金额
              use_begin_time:
                type: string
                description: 使用开始时间
              use_end_time:
                type: string
                description: 使用结束时间
              volume:
                type: integer
                description: 活动发放数量
              statistics:
                type: array
                items:
                  properties:
                    total_volume:
                      type: integer
                      description: 发放总张数
                    give_out_volume:
                      type: integer
                      description: 已分发张数
                    has_been_used_volume:
                      type: integer
                      description: 已发放张数
                    total_amount:
                      type: number
                      description: 总额
                    give_out_amount:
                      type: number
                      description: 已分发金额
                    has_been_used_amount:
                      type: number
                      description: 已使用金额

    """
    offset = int(args['offset'])
    limit = int(args['limit'])
    return CouponTypeService.coupon_type_list(company_id, offset, limit)


@bp.route('/coupon_type/add', methods=['POST'])
@post_require_check_with_permissions([])
def coupon_type_add(user_id, company_id, args):
    """
添加活动
添加活动，需要先登录
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
        condition:
          type: integer
          description: 活动领取条件 1全部用户 2新注册用户 3分享送券
        content:
          type: string
          description: 内容
        face_value:
          type: number
          description: 面值
        give_out_begin_time:
          type: string
          description: 分发开始时间
        give_out_end_time:
          type: string
          description: 分发结束时间
        img_url:
          type: string
          description: 活动图片
        is_online:
          type: integer
          description: 是否上线
        link:
          type: string
          description: 活动链接
        name:
          type: string
          description: 活动名字
        type:
          type: integer
          description: 1抵扣金额
        use_begin_time:
          type: string
          description: 使用开始时间
        use_end_time:
          type: string
          description: 使用结束时间
        volume:
          type: integer
          description: 活动发放数量
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
              description: Id
    """
    condition = args['condition']
    content = args['content']
    face_value = args['face_value']
    give_out_begin_time = args['give_out_begin_time']
    give_out_end_time = args['give_out_end_time']
    img_url = args['img_url']
    is_online = args['is_online']
    link = args['link']
    name = args['name']
    use_begin_time = args['use_begin_time']
    use_end_time = args['use_end_time']
    volume = args['volume']

    give_out_end_time = give_out_end_time.split(" ")[0] + " 23:59:59"
    use_end_time = use_end_time.split(" ")[0] + " 23:59:59"

    ret = CouponTypeService.coupon_type_add(
        company_id, condition, content, face_value,
        give_out_begin_time, give_out_end_time,
        img_url, is_online, link, name, use_begin_time, use_end_time, volume)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.ACTIVITY_ERR10)
    if ret == -11:
        raise AppError(*SubErrorCode.ACTIVITY_ERR11)
    if ret == -12:
        raise AppError(*SubErrorCode.ACTIVITY_ERR12)
    if ret == -13:
        raise AppError(*SubErrorCode.ACTIVITY_ERR13)
    if ret == -14:
        raise AppError(*SubErrorCode.ACTIVITY_ERR14)
    if ret == - 15:
        raise AppError(*SubErrorCode.ACTIVITY_ERR15)
    return ret


@bp.route('/coupon_type/change/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def coupon_type_change(user_id, company_id, args, pk):
    """
编辑活动
编辑活动，需要先登录
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
    description: ID
  - name: body
    in: body
    required: true
    schema:
      properties:
        content:
          type: string
          description: 内容
        img_url:
          type: string
          description: 活动图片
        is_online:
          type: integer
          description: 是否在线
        link:
          type: string
          description: 活动链接
        name:
          type: string
          description: 活动名字
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
              description: Id
    """
    content = args['content']
    img_url = args['img_url']
    is_online = args['is_online']
    link = args['link']
    name = args['name']
    ret = CouponTypeService.coupon_type_change(
        pk, content, img_url, is_online, link, name)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret


@bp.route('/coupon_type/offline/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def coupon_type_offline(user_id, company_id, args, pk):
    """
下线活动
下线活动，需要先登录
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
    description: ID
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
              description: Id
    """
    ret = CouponTypeService.offline(pk)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*SubErrorCode.ACTIVITY_ALREADY_OFFLINE)
    if ret == -3:
        raise AppError(*SubErrorCode.ACTIVITY_STATUS_ERR)
    return ret


@bp.route('/coupon_type/delete/<int:pk>', methods=['POST'])
@post_require_check_with_permissions([])
def coupon_type_delete(user_id, company_id, args, pk):
    """
删除活动
删除活动，需要先登录
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
    description: ID
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
              description: Id
    """
    ret = CouponTypeService.delete_coupon_type(pk)
    if ret == -1:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -2:
        raise AppError(*SubErrorCode.STATUS_ERR)
    if ret == -3:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret
