# coding:utf-8


class GlobalErrorCode(object):
    """全局错误码"""
    PARAM_ERROR = (1, u"参数错误")
    BUSINESS_ERROR = (2, u"逻辑错误")
    JSON_PARSE_ERROR = (3, u"json解析错误")
    OBJ_NOT_FOUND_ERROR = (4, u"对象找不到")
    REQUIRE_TOKEN_ERR = (5, u"需要TOKEN")
    INVALID_TOKEN_ERR = (6, u'无效的token值')
    REQUIRE_JSON_FORMAT_ERR = (7, u'需要json格式的请求体')
    PARAMS_DESERIALIZE_ERR = (8, u'参数json反序列化错误')
    MISSING_PARAM_ERR = (9, u'缺少参数 {}')
    PARAMETER_BETWEEN_ERR = (10, u'参数 page={} 取值错误, 范围 >=1')
    PARAMETER_STATUS_AND_EXPECT_ERR = (11, u'参数 status={} 取值错误, 预期值{}')
    PARAMETER_KEY_ERR = (12, u'参数{}不是{}.')
    SYSTEM_ERR = (12, u"系统错误")
    NO_PERMISSION = (13, u"没有权限")
    INVALID_PK_ERR = (14, u"无效Pk")
    DB_COMMIT_ERR = (15, u"提交错误")
    UNKNOWN_ERR = (999, u'未知错误')


class SubErrorCode(object):
    """局部错误码"""

    USER_REQUIRE_TOKEN_ERR = (200001, u"需要TOKEN")
    USER_INVALID_TOKEN_ERR = (200002, u'无效的token值')
    USER_PWD_ERR = (200003, u"密码错误")
    DEVICE_NOT_BINDING = (200004, u"设备没有绑定车辆")
    DEVICE_ALREADY_BINDING = (200005, u"设备已经绑定车辆")
    NOT_PC_USER = (200006, u"不是PC用户")
    STATUS_ERR = (200007, u"状态错误")
    ACTIVITY_ALREADY_OFFLINE = (200008, u"活动已下线,不能重复下线")
    ACTIVITY_ERR10 = (200010, u"使用结束时间应该大于使用开始时间")
    ACTIVITY_ERR11 = (200011, u"使用开始时间应该大于等于分发开始时间")
    ACTIVITY_ERR12 = (200012, u"分发结束时间应该大于分发开始时间")
    ACTIVITY_ERR13 = (200013, u"邀请新用户领取优惠券活动,数量必须为偶数")
    ACTIVITY_ERR14 = (200014, u"邀请新用户领取优惠券活动重复")
    ACTIVITY_STATUS_ERR = (200015, u"活动状态只有未开始和活动中才能下线")
    ROLE_CODE_ALREADY_EXIST = (200016, u"角色code已经存在")
    FACE_NOT_SUB_ACCOUNT = (200017, u"删除的人脸必须是子账户")
    ACTIVITY_ERR15 = (200018, u"使用结束时间应该大于等于分发结束时间")

    APP_USER_OLD_PWD_ERROR = (200041, u"您的旧密码不正确")
    APP_USER_INPUT_NOW_PWD_AND_OLD_PWD = (200042, u"请输入现在的密码和新的密码")
    APP_USER_ROLE_NOT_EXIST = (200043, u"角色不存在")
    APP_USER_VERIFICATION_CODE_ERROR = (200044, u"验证码错误")
    APP_USER_USER_NOT_FUND = (200045, u"用户找不到")
    APP_USER_PLEASE_INPUT_PWD = (200046, u"请输入密码")
    APP_USER_PLEASE_INPUT_VERIFICATION_CODE = (200047, u"请输入验证码")
    APP_USER_PLEASE_INPUT_PHONE_NUMBER = (200048, u"请输入手机号")
    APP_USER_BALANCE_INSUFFICIENT = (200049, u"余额不足,请充值")
    APP_USER_PHONE_NUMBER_ILLEGALITY = (200050, u"手机号码非法")
    APP_USER_PHONE_NUMBER_REGISTERED = (200051, u"手机号码已经注册")
    APP_USER_PHONE_NUMBER_UNREGISTER = (200051, u"手机号码未注册")
    APP_USER_ONE_MINUTE_SEND = (200052, u"请一分钟后再次发送")
    APP_USER_VERIFICATION_CODE_SENDING_FAIL = (200053, u"验证码发送失败")
    APP_USER_PWD_ERROR = (200054, u"密码错误")
    APP_USER_ALREADY_EXIST = (200055, u"用户已经存在")
    APP_USER_IN_BAIDU_NOT_FOUND = (200056, u"用户没有在百度人脸库找到")

    APP_COUPON_STATUS_ERR = (200056, u"优惠券状态错误")
    APP_COUPON_ACTIVITY_NOT_STARTING = (200057, u"活动还没有开始")
    APP_CERT_REPETITION_REGISTER_FACE = \
        (200058, u"不能重复注册人脸,请先删除以前的子账户或关闭账号")
    APP_USER_ALREADY_REGISTERED_FACE = (200059, u"用户已经注册人脸")
    APP_COUPON_CODE_ERR = (200060, u"优惠券code错误")

    DEVICE_UNKNOWN_ERROR = (200091, u"设备未知错误")
    DEVICE_UNREGISTER_FACE = (200092, u"未注册人脸")
    DEVICE_RECOGNITION_FAILED = (200093, u"识别失败")
    DEVICE_VERIFY_SIGN_FAIL = (200094, u"验签失败")
    DEVICE_NOT_ENABLE_FACE_FUNCTION = (200095, u"未开启人脸功能")
    DEVICE_GET_TOKEN_ERROR = (200096, u"获取token错误")
    DEVICE_REPEAT_SWIPING_FACE = (200097, u"重复刷脸")
    DEVICE_NOT_FOUND_ERROR = (200098, u"根据上送的设备号找不到设备")
    DEVICE_NOT_FOUND_SUB_ACCOUNT = (200099, u"未在数据库找到该子账户")
    DEVICE_GPS_CONVERSION_ERROR = (200100, u"设备上送GPS转换错误")

    CERT_IDENTITY_ALREADY_BINDING_USER = (200201, u"该身份已经绑定用户")
    CERT_REPETITION_COMMIT = (200081, u"重复提审")
    CERT_IDENTITY_REPEAT = (200082, u"身份重复")

    ADMIN_USER_PWD_ERROR = (200100, u"密码错误")
    ADMIN_USER_PERMISSION_GT_COMPANY = (200101, u"用户权限大于公司权限")

    CAR_NOT_BINDING_ROUTE = (200201, u"车辆没有绑定线路")

    # 线路200210 - 200219
    ROUTE_NAME_ONLY_NUMBERS = (200210, u"线路名字只能是数字")
    ROUTE_ALREADY_DISABLED = (200211, u"线路已经禁用,车辆无法绑定该线路")

    # 权限200220 - 200229
    PERMISSION_PRIVILEGE_SET = (200220, u"权限集合错误")

    # 小程序 200230 - 200239
    MINI_DECRYPT_FAIL = (200230, u"小程序解析code失败")

    # 人脸 200240 - 200249
    FACE_UPLOAD_IMAGE_NOT_FACE = (200240, u"上传的图片不是人脸")


ORDER_STATUS = dict(
    valid=1,    # 有效
    delete=10   # 删除
)

OPERATION_CODE = dict(
    list='LIST',
    create='CREATE',
    retrieve='RETRIEVE',
    update='UPDATE',
    destroy='DESTROY'
)

ROLE_CODE = dict(
    super_admin='SUPER_ADMIN',
    admin='ADMIN',
    emp='EMP'
)

ENTERPRISE_LEVEL = dict(
    parent=1,
    child=2,
)