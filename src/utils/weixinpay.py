# coding:utf-8

import time
import json
from weixin.pay import WeixinPay
from lxml import etree
from ext import conf


def get_wein_pay(platform_type):
    weixin_config = conf.config['WEI_XIN']
    # 小程序
    if platform_type == 2:
        weixin_config["app_id"] = conf.config['MINI_APP_ID']
    pay = WeixinPay(**weixin_config)
    return pay


def get_unified_ordering(data, spbill_create_ip, platform_type=1, openid=""):
    """
    :param data:
    :param spbill_create_ip:
    :param platform_type: 1:APP 2:小程序
    :return:
    """

    pay = get_wein_pay(platform_type)

    # pay.PAY_HOST = 'https://api.mch.weixin.qq.com/sandboxnew'

    # res_dci = {
    #     'nonce_str': pay.nonce_str,
    #     'mch_id': weixin_config['mch_id']
    # }
    # res_dci['sign'] = pay.sign(res_dci)
    # resp = pay.sess.post(
    #     'https://api.mch.weixin.qq.com/sandboxnew/pay/getsignkey', data=pay.to_xml(res_dci))
    # resp_dict = pay.to_dict(resp.content.decode('utf-8'))
    # logger.debug(resp_dict)

    # weixin_config['mch_key'] = resp_dict['sandbox_signkey']
    # pay = WeixinPay(**weixin_config)

    # pay.PAY_HOST = 'https://api.mch.weixin.qq.com/sandboxnew'
    if platform_type == 1:
        trade_type = 'APP'
        attach = {"platform_type": 1}
    elif platform_type == 2:
        trade_type = 'JSAPI'
        attach = {"platform_type": 2}
    unified_order = dict(trade_type=trade_type,
                         body=data.get('name', u'充值'),
                         out_trade_no=str(data.get('order_no', '')),
                         total_fee=int(float(data.get('amount', '')) * 100),
                         spbill_create_ip=spbill_create_ip,
                         attach=json.dumps(attach))
    if openid:
        unified_order["openid"] = openid

    try:
        raw = pay.unified_order(**unified_order)
        if pay.check(raw):
            if platform_type == 2:
                result = {
                    'appId': pay.app_id,
                    'timeStamp': str(int(time.time())),
                    'nonceStr': raw['nonce_str'],
                    'package': "prepay_id=" + raw["prepay_id"],
                    'signType': 'MD5'
                }
            if platform_type == 1:
                result = {
                    'appid': pay.app_id,
                    'partnerid': pay.mch_id,
                    'prepayid': raw['prepay_id'],
                    'package': 'Sign=WXPay',
                    'noncestr': raw['nonce_str'],
                    'timestamp': str(int(time.time())),
                }

            result['sign'] = pay.sign(result)
            return result
        else:
            return -10
    except Exception as err:
        print err
        return -10


def xml_to_dict(content):
    raw = {}
    root = etree.fromstring(content.encode("utf-8"),
                            parser=etree.XMLParser(resolve_entities=False))
    for child in root:
        raw[child.tag] = child.text
    return raw


def dict_to_xml(raw):
    s = ""
    for k, v in raw.items():
        s += "<{0}><![CDATA[{1}]]></{0}>".format(k, v)
    s = "<xml>{0}</xml>".format(s)
    return s
