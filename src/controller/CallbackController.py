# coding:utf-8

import json
from flask import request
from sqlalchemy import and_
from decimal import Decimal
from datetime import datetime
from flask.blueprints import Blueprint
from flask import Response
from sqlalchemy.exc import SQLAlchemyError

from core.framework import get_require_check_with_permissions, \
    post_require_check_with_permissions, post_require_check
from core.AppError import AppError
from utils.defines import SubErrorCode, GlobalErrorCode

from service.CallbackService import CallbackService
from utils import scan
from utils import pay

try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('CallbackController', __name__)
"""蓝图url前缀"""
url_prefix = '/callback'


@bp.route('/ali-recharge/', methods=['POST'])
def alipay_callback():
    req_args = request.values.to_dict()
    # 验签失败
    if not pay.verify_sign(req_args):
        print u"验签失败"
        return 'failure'

    out_trade_no = req_args['out_trade_no']
    trade_no = req_args['trade_no']
    trade_status = req_args.get('trade_status', None)
    total_amount = req_args.get('total_amount', None)
    gmt_payment = req_args.get('gmt_payment', None)
    result = CallbackService.alipay_callback(
        out_trade_no, trade_no, trade_status, total_amount, gmt_payment)
    response = Response(result)
    response.status_code = 200
    return response


@bp.route('/weixin-recharge/', methods=['POST'])
def weixin_callback():
    req_args = request.get_data()
    xml = CallbackService.weixinpay_callback(req_args)
    response = Response(xml)
    response.content_type = 'text/xml'
    response.status_code = 200
    return response


def google_gps_to_gorde_gpd(longitude, latitude):
    s = longitude + "," + latitude
    url = "https://restapi.amap.com/v3/assistant/coordinate/convert?" \
          "key=5c96c771bb5621b2bc0f80130e56b083&locations={}" \
          "&coordsys=gps".format(s)
    res = requests.get(url)
    d = json.loads(res.content.decode("utf-8"))
    if "locations" not in d:
        return 0, 0
    arr = d['locations'].split(",")
    return arr[0], arr[1]


@bp.route('/facergn-callback/', methods=['POST'])
@post_require_check([])
def face_rgn_callback(args):
    """
人脸订单回调
人脸订单回调，需要先登录
---
tags:
  - 设备
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
        device_no:
          type: string
          description: 设备号
        up_stamp:
          type: integer
          description: 上送时间戳
        mobile:
          type: string
          description: 手机号
        longitude:
          type: number
          description: 经度
        latitude:
          type: number
          description: 纬度
        verify_type:
          type: integer
          description: 此接口填写2
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
          description: 状态 0正常 1参数错误 200094验签失败 200095未开启人脸功能 200049余额不足 200097重复刷脸 200098根据上送的设备号找不到设备
        data:
          type: object
          properties:
            mobile:
              type: string
              description: 手机号
            amounts:
              type: number
              description: 用户余额
    """
    data = request.values.to_dict()
    print data
    device_no = data["device_no"]
    up_stamp = data["up_stamp"]
    mobile = data["mobile"]
    longitude = data["longitude"]
    latitude = data["latitude"]
    verify_type = int(data["verify_type"])

    # 验证签名
    if not isinstance(data, dict):
        if not scan.verify_sign(data):
            raise AppError(*SubErrorCode.DEVICE_VERIFY_SIGN_FAIL)

    # 替换gps
    try:
        longitude, latitude = \
            google_gps_to_gorde_gpd(longitude, latitude)
    except:
        raise AppError(*SubErrorCode.DEVICE_GPS_CONVERSION_ERROR)
    sub_account = None
    if len(mobile) > 11:
        sub_account = mobile
        mobile = mobile[:11]

    # 不是人脸请求直接报错
    if verify_type and verify_type != 2:
        raise AppError(*GlobalErrorCode.PARAM_ERROR)

    try:
        scan_time = datetime.fromtimestamp(float(up_stamp))
    except ValueError:
        raise AppError(*GlobalErrorCode.PARAM_ERROR)

    ret = CallbackService.face_callback(
        device_no, scan_time, mobile, verify_type, sub_account)
    if ret == -10:
        raise AppError(*SubErrorCode.DEVICE_NOT_FOUND_ERROR)
    if ret == -11:
        raise AppError(*SubErrorCode.DEVICE_REPEAT_SWIPING_FACE)
    if ret == -12:
        raise AppError(*SubErrorCode.DEVICE_NOT_FOUND_SUB_ACCOUNT)
    if ret == -13:
        raise AppError(*SubErrorCode.DEVICE_NOT_ENABLE_FACE_FUNCTION)
    if ret == -14:
        raise AppError(*SubErrorCode.APP_USER_BALANCE_INSUFFICIENT)
    if ret == -15:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret


@bp.route('/qrcode-callback/', methods=['POST'])
@post_require_check(['longitude'])
def qrcode_callback(args):
    """
二维码订单回调
二维码订单回调，需要先登录
---
tags:
  - 设备
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
        device_no:
          type: string
          description: 设备号
        up_stamp:
          type: integer
          description: 上送时间戳
        mobile:
          type: string
          description: 手机号
        longitude:
          type: number
          description: 经度
        latitude:
          type: number
          description: 纬度
        verify_type:
          type: integer
          description: 此接口填写1
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
          description: 状态 0正常 1参数错误 200094验签失败 200049余额不足 200098根据上送的设备号找不到设备
        data:
          type: object
          properties:
            mobile:
              type: string
              description: 手机号
            amounts:
              type: number
              description: 用户余额
    """
    data = args
    longitude = data["longitude"]
    latitude = data["latitude"]
    # 验证签名
    if not isinstance(data, dict):
        if not scan.verify_sign(data):
            raise AppError(*SubErrorCode.DEVICE_VERIFY_SIGN_FAIL)

    device_no = data["device_no"]
    up_stamp = data["up_stamp"]
    mobile = data["mobile"]
    verify_type = int(data["verify_type"])
    # 不是无感行二维码请求直接报错
    if verify_type != 1:
        raise AppError(*GlobalErrorCode.PARAM_ERROR)

    try:
        up_time = datetime.fromtimestamp(float(up_stamp))
    except ValueError:
        raise AppError(*GlobalErrorCode.PARAM_ERROR)
    print(str(data))
    ret = CallbackService.qrcode_callback(mobile, device_no, up_time,
                                          verify_type, longitude, latitude)
    if ret == -10:
        raise AppError(*SubErrorCode.DEVICE_NOT_FOUND_ERROR)
    if ret == -11:
        raise AppError(*SubErrorCode.APP_USER_BALANCE_INSUFFICIENT)
    if ret == -15:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret


@bp.route('/gps/', methods=['POST'])
@post_require_check([])
def gps_callback(args):
    """
    gps
    """
    data = request.values.to_dict()
    device_no = data["device_no"]
    longitude = data["longitude"]
    latitude = data["latitude"]
    timestamp = data['timestamp']
    CallbackService.gps_callback(device_no, longitude, latitude, timestamp)
    return {}
