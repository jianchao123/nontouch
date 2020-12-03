# coding:utf-8
import logging
from alipay.aop.api.util.SignatureUtils import verify_with_rsa
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest

from app import app

logger = logging.getLogger(__name__)


def verify_sign(params):
    sign = params.pop('sign', None)
    params.pop('sign_type')
    params = sorted(params.items(), key=lambda e: e[0], reverse=False)
    message = "&".join(u"{}={}".format(k, v) for k, v in params).encode()
    try:
        return verify_with_rsa(app.config['ALIPAY_PUBLIC_KEY'], message, sign)
    except Exception as err:
        print err
        return False


def add_sign(params):
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = app.config['ALIPAY_GATEWAY']
    alipay_client_config.app_id = app.config['APP_ID']
    alipay_client_config.app_private_key = app.config['APP_PRIVATE_KEY']
    alipay_client_config.alipay_public_key = app.config['ALIPAY_PUBLIC_KEY']

    client = DefaultAlipayClient(
        alipay_client_config=alipay_client_config, logger=logger)

    model = AlipayTradeAppPayModel()

    model.timeout_express = "15m"
    model.total_amount = str(params['amount'])
    # model.seller_id = "2088301194649043"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.subject = params['name']
    if params.get('body', None):
        model.body = params['body']
    model.out_trade_no = params['order_no']

    request = AlipayTradeAppPayRequest(biz_model=model)
    request.notify_url = app.config['NOTIFY_URL']

    response = client.sdk_execute(request)

    return response
