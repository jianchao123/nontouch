# coding:utf-8
try:
    from flask import request
    from flask.blueprints import Blueprint
    from core.framework_1 import post_require_check, get_require_check, \
        get_require_check_with_user, post_require_check_with_user
    from core.AppError import AppError
    from utils.defines import GlobalErrorCode, SubErrorCode
    from service.ClientAppService import ClientAppService
    from ext import conf
except:
    import traceback
    print traceback.format_exc()
try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('AppController', __name__)
"""蓝图url前缀"""
url_prefix = '/api/v1'


@bp.route('/register/', methods=['POST'])
@post_require_check(['mobile', 'password', 'code'])
def register(args):
    """
注册用户
注册用户
---
tags:
  - APP
parameters:
  - name: password
    in: query
    type: string
    required: true
    description: 密码
  - name: mobile
    in: query
    type: string
    required: true
    description: 手机号
  - name: code
    in: query
    type: string
    required: true
    description: 验证码
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
              description: 新注册的用户Id
    """
    mobile = args['mobile']
    password = args['password']
    code = args['code']
    invite_code = args.get('invite_code', None)
    ret = ClientAppService.signup(mobile, password, code, invite_code)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.APP_USER_ALREADY_EXIST)
    if ret == -11:
        raise AppError(*SubErrorCode.APP_USER_VERIFICATION_CODE_ERROR)
    return ret


@bp.route('/login/', methods=['POST'])
@post_require_check(['mobile', 'password'])
def login(args):
    """
登录
登录
---
tags:
  - APP
parameters:
  - name: mobile
    in: query
    type: string
    required: true
    description: 手机号
  - name: password
    in: query
    type: string
    required: true
    description: 密码

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
            token:
              type: string
              description: TOKEN
    """
    mobile = args['mobile']
    password = args['password']

    if mobile == '' or password == '':
        raise AppError(*SubErrorCode.USER_PWD_ERR)

    ret = ClientAppService.signin(mobile, password)
    if ret == -1:
        raise AppError(*SubErrorCode.USER_PWD_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.USER_PWD_ERR)

    return ret


@bp.route('/code/', methods=['POST'])
@post_require_check(['mobile', 'type'])
def send_verify_code(args):
    """
发送验证码
发送验证码
---
tags:
  - APP
parameters:
  - name: mobile
    in: query
    type: string
    required: true
    description: 手机号
  - name: type
    in: query
    type: integer
    required: true
    description: 1注册 2修改密码 3登陆

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
            token:
              type: string
              description: 空json
    """
    mobile = args['mobile']
    code_type = int(args['type'])
    ret = ClientAppService.send_verify_code(mobile, code_type)
    if ret == -4:
        raise AppError(*GlobalErrorCode.PARAM_ERROR)
    if ret == -10:
        raise AppError(*SubErrorCode.APP_USER_PHONE_NUMBER_ILLEGALITY)
    if ret == -11:
        raise AppError(*SubErrorCode.APP_USER_PHONE_NUMBER_REGISTERED)
    if ret == -12:
        raise AppError(*SubErrorCode.APP_USER_PHONE_NUMBER_UNREGISTER)
    if ret == -13:
        raise AppError(*SubErrorCode.APP_USER_ONE_MINUTE_SEND)
    if ret == -14:
        raise AppError(*SubErrorCode.APP_USER_VERIFICATION_CODE_SENDING_FAIL)
    return ret


@bp.route('/me/', methods=['GET'])
@get_require_check_with_user([])
def user_info(user_id, args):
    """
个人用户信息
个人用户信息
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
          type: object
          properties:
            id:
              type: integer
              description: PK
            mobile:
              type: string
              description: 手机号
            nickname:
              type: string
              description: 昵称
            balance:
              type: number
              description: 余额
            avatar:
              type: string
              description: 头像
            gender:
              type: integer
              description: 性别
            birthday:
              type: string
              description: 生日(日期格式)
            is_open_face_rgz:
              type: integer
              description: 是否开启人脸
            is_recharge:
              type: integer
              description: 是否充值超过5元
            coupon_number:
              type: integer
              description: 优惠券数量

    """
    return ClientAppService.user_info(user_id)


@bp.route('/me/change/', methods=['POST'])
@post_require_check_with_user([])
def change_user_info(user_id, args):
    """
修改个人信息
修改个人信息，需要先登录
---
tags:
  - APP
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
        nickname:
          type: string
          description: 昵称
        avatar:
          type: string
          description: 头像
        gender:
          type: integer
          description: 性别
        birthday:
          type: string
          description: 生日(日期格式)
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
              description: 修改成功用户id
    """
    nickname = args.get('nickname', None)
    avatar = args.get('avatar', None)
    gender = args.get('gender', None)
    birthday = args.get('birthday', None)
    ret = ClientAppService.change_user(
        user_id, nickname, avatar, gender, birthday)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret


@bp.route('/findpassword/', methods=['POST'])
@post_require_check(['mobile', 'password', 'code'])
def forget_pwd(args):
    """
忘记密码
忘记密码，需要先登录
---
tags:
  - APP
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
        mobile:
          type: string
          description: 手机号
        password:
          type: string
          description: 密码
        code:
          type: string
          description: 验证码
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
              description: 修改成功用户id
    """
    mobile = args['mobile']
    password = args['password']
    code = args['code']
    ret = ClientAppService.forget_pwd(mobile, code, password)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*GlobalErrorCode.OBJ_NOT_FOUND_ERROR)
    if ret == -11:
        raise AppError(*SubErrorCode.APP_USER_VERIFICATION_CODE_ERROR)
    return ret


@bp.route('/gencode/', methods=['POST'])
@get_require_check_with_user([])
def qrcode(user_id, args):
    """
获取乘车二维码
获取乘车二维码，需要先登录
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
          type: object
          properties:
            qrcode:
              type: string
              description: 乘车二维码
    """
    ret = ClientAppService.get_qrcode(user_id)
    if ret == -10:
        raise AppError(*SubErrorCode.APP_USER_BALANCE_INSUFFICIENT)
    return ret


@bp.route('/coupons/', methods=['GET'])
@get_require_check_with_user([])
def coupons_api(user_id, args):
    """
优惠券列表
优惠券列表，需要先登录
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
          type: object
          properties:
            id:
              type: integer
              description: PK
            use_begin_time:
              type: string
              description: 此次活动优惠券的使用开始时间
            use_end_time:
              type: string
              description: 此次活动优惠券的使用结束时间
            img_url:
              type: string
              description: 图片
            name:
              type: string
              description: 优惠券名字
            face_value:
              type: number
              description: 面值
            status:
              type: 状态
              description: 1 未发放 2 已发放 3 已使用 4 过期
            code:
              type: string
              description: 券码

    """
    status = args['status']
    return ClientAppService.user_coupon_list(user_id, status)


@bp.route('/coupon/add/', methods=['POST'])
@post_require_check_with_user(['code'])
def receive_coupon(user_id, args):
    """
领取优惠券
领取优惠券，需要先登录
---
tags:
  - APP
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
        code:
          type: string
          description: 券码
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
              description: 领取成功的优惠券id
    """
    code = args['code']
    ret = ClientAppService.receive_coupon(user_id, code)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.APP_COUPON_STATUS_ERR)
    if ret == -11:
        raise AppError(*SubErrorCode.APP_COUPON_ACTIVITY_NOT_STARTING)
    if ret == -12:
        raise AppError(*SubErrorCode.APP_COUPON_CODE_ERR)
    return ret


@bp.route('/openfacerecognition/', methods=['GET'])
@get_require_check_with_user([])
def open_face_recognition_retrieve(user_id, args):
    """
是否开启人脸识别
是否开启人脸识别，需要先登录
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
          type: object
          properties:
            is_open_face_rgz:
              type: integer
              description: 是否开启人脸识别 1是 0否
    """
    return ClientAppService.get_user_face_status(user_id)


@bp.route('/openfacerecognition/', methods=['POST'])
@post_require_check_with_user(['open_or_close'])
def open_face_recognition(user_id, args):
    """
打开和关闭人脸
打开和关闭人脸，需要先登录
---
tags:
  - APP
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
        open_or_close:
          type: integer
          description: 1开启 0关闭
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
              description: 用户id
    """
    open_or_close = args['open_or_close']
    ret = ClientAppService.open_face_recognition(user_id, open_or_close)
    return ret


@bp.route('/faceimg/', methods=['GET'])
@get_require_check_with_user([])
def face_image_info(user_id, args):
    """
个人帐号人脸信息查询
个人帐号人脸信息查询，需要先登录
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
          type: object
          properties:
            id:
              type: integer
              description: PK
            baidu_user_id:
              type: string
              description: 手机号
            oss_url:
              type: string
              description: 人脸url
            parent_mobile:
              type: string
              description: 父级手机号
            is_sub_account:
              type: integer
              description: 是否子帐号
            sub_account_name:
              type: string
              description: 子帐号名字

    """
    return ClientAppService.face_image_list(user_id)


@bp.route('/faceimg/change/<string:baidu_user_id>/', methods=['POST'])
@post_require_check_with_user([])
def face_image_change_api(user_id, args, baidu_user_id):
    """
个人帐号人脸信息查询
个人帐号人脸信息查询，需要先登录
---
tags:
  - APP
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: baidu_user_id
    in: path
    type: string
    required: true
    description: 主帐号或者子帐号
  - name: body
    in: body
    required: true
    schema:
      properties:
        oss_url:
          type: string
          description: 人脸url
        sub_account_name:
          type: string
          description: 子帐号名字
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
              description: 修改成功的PK
    """
    print args
    oss_url = args.get('oss_url', None)
    sub_account_name = args.get('sub_account_name', None)
    ret = ClientAppService.face_image_change(
        user_id, baidu_user_id, oss_url, sub_account_name)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.APP_USER_IN_BAIDU_NOT_FOUND)
    return ret


@bp.route('/faceimg/delete/<int:pk>/', methods=['POST'])
@post_require_check_with_user([])
def face_image_delete(user_id, args, pk):
    """
删除子帐号
删除子帐号，需要先登录
---
tags:
  - APP
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
    description: 需要删除的faceimg的Pk
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
              description: 删除成功的PK

    """
    ret = ClientAppService.face_image_delete(pk)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.STATUS_ERR)
    if ret == -11:
        raise AppError(*SubErrorCode.FACE_NOT_SUB_ACCOUNT)
    return ret


@bp.route('/faceimg/add/', methods=['POST'])
@post_require_check_with_user(['oss_url', 'is_sub_account'])
def face_image_add_api(user_id, args):
    """
人脸图片上传百度
人脸图片上传百度，需要先登录
---
tags:
  - APP
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
        oss_url:
          type: string
          description: 人脸oss url
        is_sub_account:
          type: string
          description: 是否子账户 1是 0否
        sub_account_name:
          type: string
          description: 子账户名字
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
              description: PK
            baidu_user_id:
              type: string
              descrition: 手机号
            group_id:
              type: integer
              description: 百度人脸分组id
            oss_url:
              type: string
              description: 人脸图片
            parent_mobile:
              type: string
              description: 父级手机号
            sub_account_name:
              type: string
              description: 子账户名字
            is_sub_account:
              type: integer
              description: 是否子账户 1是 0否
            face_id:
              type: integer
              description: 百度FACE TOKEN
            face_last_time:
              type: string
              description: 最后更新时间
            user_id:
              type: integer
              description: 用户id
            status:
              type: integer
              description: 状态 1有效 10删除

    """
    oss_url = args['oss_url']
    is_sub_account = int(args['is_sub_account'])
    sub_account_name = args.get('sub_account_name', None)

    ret = ClientAppService.face_image_add(
        user_id, oss_url, is_sub_account, sub_account_name)
    if ret == -10:
        raise AppError(*SubErrorCode.APP_CERT_REPETITION_REGISTER_FACE)
    if ret == -11:
        raise AppError(*SubErrorCode.APP_USER_ALREADY_REGISTERED_FACE)
    return ret


@bp.route('/recharges/', methods=['GET'])
@get_require_check_with_user([])
def user_recharges(user_id, args):
    """
用户充值记录
用户充值记录，需要先登录
---
tags:
  - APP
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: is_open_bill
    in: query
    type: integer
    description: 1-已开具的 2-未开具的 [可空]
  - name: last_pk
    in: query
    type: integer
    required: true
    description: 最后一条记录的id,第一次传99999999
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
            pk:
              type: integer
              description: id
            user_id:
              type: integer
              description: 用户id
            name:
              type: string
              description: 名字
            amount:
              type: number
              description: 充值金额
            pay_type:
              type: integer
              description: 支付方式 1支付宝 2微信 3银联
            to_whom:
              type: string
              description: 代充手机号
            order_no:
              type: string
              description: 订单号
            status:
              type: integer
              description: 订单状态 1待支付 2成功 3失败
            create_time:
              type: string
              description: 创建时间
    """
    is_open_bill = args.get('is_open_bill', None)
    last_pk = args['last_pk']
    return ClientAppService.user_recharges(user_id, is_open_bill, last_pk)


@bp.route('/recharges/add/', methods=['POST'])
@post_require_check_with_user([])
def user_recharge_add(user_id, args):
    """
统一下单接口
统一下单接口，需要先登录
---
tags:
  - APP
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
          description: 充值订单名字
        pay_type:
          type: integer
          description: 支付方式1支付宝 2微信 3银联
        amount:
          type: number
          description: 充值金额
        to_whom:
          type: string
          required: false
          description: 代充帐号

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
            appid:
              type: string
              description: appid
            partnerid:
              type: string
              description: partnerid
            prepayid:
              type: string
              description: prepayid
            package:
              type: string
              description: package
            noncestr:
              type: string
              description: noncestr
            timestamp:
              type: string
              description: 时间戳
            appId:
              type: string
              description: JSAPI appId
            timeStamp:
              type: string
              description: JSAPI 时间戳
            nonceStr:
              type: string
              description: JSAPI nonceStr
            signType:
              type: string
              description: JSAPI 默认MD5

    """
    name = args['name']
    pay_type = int(args['pay_type'])
    amount = float(args['amount'])
    to_whom = args.get('to_whom', None)
    remote_addr = request.remote_addr
    token = request.headers.get('token')
    amount = 0.01
    is_mini = 0
    if 'MINI' in token:
        is_mini = 1
    ret = ClientAppService.user_recharge_add(
        user_id, name, pay_type, amount, to_whom, remote_addr, is_mini)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret


@bp.route('/recharges/change/<string:order_no>/', methods=['POST'])
@post_require_check_with_user([])
def user_recharge_change(user_id, args, order_no):
    """
统一下单接口(补充)
统一下单接口(补充)，需要先登录
---
tags:
  - APP
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: order_no
    in: path
    type: string
    required: true
    description: 订单号

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
            appid:
              type: string
              description: appid
            partnerid:
              type: string
              description: partnerid
            prepayid:
              type: string
              description: prepayid
            package:
              type: string
              description: package
            noncestr:
              type: string
              description: noncestr
            timestamp:
              type: string
              description: 时间戳
            appId:
              type: string
              description: JSAPI appId
            timeStamp:
              type: string
              description: JSAPI 时间戳
            nonceStr:
              type: string
              description: JSAPI nonceStr
            signType:
              type: string
              description: JSAPI 默认MD5

    """
    return ClientAppService.user_recharge_change(order_no, request.remote_addr)


@bp.route('/orders/', methods=['GET'])
@get_require_check_with_user([])
def orders(user_id, args):
    """
乘车记录
乘车记录，需要先登录
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
          type: object
          properties:
            pay_type:
              type: integer
              description: 支付方式 1支付宝 2微信 3银联 4余额
            state:
              type: integer
              description: 1-待支付 2-成功 3-失败
            station:
              type: integer
              description: 站点名字
            discount_way:
              type: integer
              description: 0无优惠  1身份  2优惠券  3免费
            real_amount:
              type: number
              description: 实付金额
            discount:
              type: number
              description: 折扣金额
            verify_type:
              type: integer
              description: 1-无感行二维码 2-人脸 3-IC卡
    """
    return ClientAppService.user_orders(user_id)


@bp.route('/getststoken/', methods=['GET'])
@get_require_check_with_user([])
def getststoken(user_id, args):
    d = dict()
    d["BUCKET"] = conf.config["OSS_BUCKET"]
    d["REGION"] = conf.config['OSS_REGION']
    d["ENDPOINT"] = conf.config['OSS_POINT']
    d["OSS_ALL_KEY"] = conf.config['OSS_ALL_KEY']
    d["OSS_ALL_SECRET"] = conf.config['OSS_ALL_SECRET']
    return d


@bp.route('/districtcode/list', methods=['GET'])
@get_require_check([])
def districtcode_list(user_id, company_id, args):
    """
区域代码
区域代码
---
tags:
  - 共用接口
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
    return ClientAppService.district_code_list()


@bp.route('/apps/', methods=['GET'])
@get_require_check([])
def get_app_version(args):
    """
    """
    return ClientAppService.app_version()


@bp.route('/feedbacks/', methods=['POST'])
@post_require_check_with_user([])
def feedback_add_api(user_id, args):
    """
    """
    content = args['content']
    ret = ClientAppService.feedback_add(user_id, content)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret


@bp.route('/notices/', methods=['GET'])
@get_require_check([])
def notices_list_api(args):
    """
    """
    start_time = args['start_time']
    return ClientAppService.notice_list(start_time)


@bp.route('/adverts/', methods=['GET'])
@get_require_check([])
def advert_list_api(args):
    """
    """
    adv_location = args.get('adv_location', None)
    return ClientAppService.advert_list(adv_location)


@bp.route('/lostandfounds/', methods=['GET'])
@get_require_check_with_user([])
def lostandfounds_list_api(user_id, args):
    """
失物招领列表
失物招领列表，需要先登录
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
                type: integer
                description: id

    """
    is_query_me = args.get('is_query_me', None)
    return ClientAppService.lostandfound_list(user_id, is_query_me)


@bp.route('/lostandfounds/add/', methods=['POST'])
@post_require_check_with_user([])
def lostandfounds_add_api(user_id, args):
    """
创建失物招领信息
创建失物招领列表信息，需要先登录
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
                type: integer
                description: id

    """
    description = args['description']
    city = args['city']
    line_no = args['line_no']
    contacts = args['contacts']
    imgs = args['imgs']
    ret = ClientAppService.lostandfound_add(
        user_id, description, city, line_no, contacts, imgs)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret


@bp.route('/lostandfounds/change/<int:pk>/', methods=['POST'])
@post_require_check_with_user([])
def lostandfounds_change_api(user_id, args, pk):
    """
更新失物招领信息
更新失物招领列表信息，需要先登录
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
                type: integer
                description: id
    """
    status = args['status']
    return ClientAppService.lostandfound_change(pk, status)


@bp.route('/lostandfounds/retrieve/<int:pk>/', methods=['GET'])
@get_require_check_with_user([])
def lostandfounds_retrieve_api(user_id, args, pk):
    """
检索失物招领
检索失物招领列表，需要先登录
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
                type: integer
                description: id
    """
    return ClientAppService.lostandfound_retrieve(pk, user_id)


@bp.route('/certification/identities/', methods=['GET'])
@get_require_check_with_user([])
def identity_list_api(user_id, args):
    """
查询该公司所有可申请身份
查询该公司所有可申请身份，需要先登录
---
tags:
  - APP
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: company
    in: query
    type: integer
    description: 公司id
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

    """
    company_id = args['company']
    return ClientAppService.identity_list(company_id)


@bp.route('/certification/certification/', methods=['GET'])
@get_require_check_with_user([])
def certification_list_api(user_id, args):
    """
审核列表
审核列表，需要先登录
---
tags:
  - APP
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: company
    in: query
    type: integer
    description: 公司id
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

    """
    return ClientAppService.certification_list(user_id)


@bp.route('/certification/certification/', methods=['POST'])
@post_require_check_with_user([])
def certification_commit_api(user_id, args):
    """
申请身份
申请身份，需要先登录
---
tags:
  - APP
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
        company:
          type: integer
          description: 公司id
        identity_id:
          type: integer
          description: 身份Id
        upload_imgs:
          type: string
          description: 图片 逗号分割
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
              description: 新增的审核Id


    """
    company_id = args['company']
    identity_id = args['identity']
    upload_imgs = args['upload_imgs']
    ret = ClientAppService.certification_commit(
        company_id, identity_id, user_id, upload_imgs)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    if ret == -10:
        raise AppError(*SubErrorCode.CERT_REPETITION_COMMIT)
    return ret


@bp.route('/certification/query_company/', methods=['GET'])
@get_require_check_with_user([])
def cert_query_company_api(user_id, args):
    """
公司列表
公司列表，需要先登录
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
                type: integer
                description: id

    """
    return ClientAppService.cert_query_company(user_id)


@bp.route('/bills/', methods=['POST'])
@post_require_check_with_user([])
def create_bill_api(user_id, args):
    """
创建票据
创建票据，需要先登录
---
tags:
  - APP
parameters:
  - name: token
    in: header
    type: string
    required: true
    description: TOKEN
  - name: headline
    in: query
    type: string
    description: 抬头
  - name: headline_type
    in: query
    type: integer
    description: 抬头类型
  - name: bank_name
    in: query
    type: string
    description: 开户行
  - name: bank_account
    in: query
    type: string
    description: 银行账户
  - name: email
    in: query
    type: string
    description: 邮箱
  - name: enterprise_name
    in: query
    type: string
    description: 企业名字
  - name: bill_no
    in: query
    type: string
    description: 票号
  - name: enterprise_address
    in: query
    type: string
    description: 企业地址
  - name: enterprise_phone
    in: query
    type: string
    description: 企业电话
  - name: recharge_pks
    in: query
    type: string
    description: 充值记录的id字符串,逗号拼接

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


    """
    headline = args['headline']
    headline_type = args['headline_type']
    bank_name = args.get('bank_name', None)
    bank_account = args.get('bank_account', None)
    email = args['email']
    enterprise_name = args.get('enterprise_name', None)
    bill_no = args.get('bill_no', None)
    enterprise_address = args.get('enterprise_address', None)
    enterprise_phone = args.get('enterprise_phone', None)
    recharge_pks = args['recharge_pks']
    if len(email) > 16:
        raise AppError(*GlobalErrorCode.PARAM_ERROR)

    ret = ClientAppService.create_bill(
        user_id, headline, headline_type, bank_name, bank_account,
        email, enterprise_name, bill_no, enterprise_address,
        enterprise_phone, recharge_pks)
    if ret == -2:
        raise AppError(*GlobalErrorCode.DB_COMMIT_ERR)
    return ret