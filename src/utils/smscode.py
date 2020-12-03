# coding:utf-8
import logging
import string
import json
import random

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from ext import conf

logger = logging.getLogger(__name__)
ALL_LETTERS = string.ascii_uppercase+string.digits


def randomCode(length=6):
    return ''.join(random.choice(string.digits) for i in range(length))


def send_code_ali(mobile, code, type=1):

    config = conf.config["ALIYUN_VERIFY_CODE"]

    client = AcsClient(config['accessKeyId'],
                       config['accessSecret'], 'default')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('PhoneNumbers', mobile)
    request.add_query_param('SignName', config['SignName'])
    if type == 1:
        request.add_query_param('TemplateCode', config['register_template_code'])
    elif type == 2:
        request.add_query_param('TemplateCode', config['password_template_code'])
    elif type == 3:
        request.add_query_param('TemplateCode', config['login_template_code'])
    request.add_query_param('TemplateParam', '{"code": "%s"}' % code)

    response = client.do_action(request)
    res = json.loads(response.encode('utf-8'))
    info_text = u'发送验证码 {} 给 {} %s'.format(code, mobile)
    if res['Code'] == 'OK':
        logger.info(info_text, u'成功')
        return True
    return False
