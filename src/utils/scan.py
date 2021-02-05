# coding:utf-8
import time
import hashlib
# import pyotp
from Crypto.Hash import SHA
from utils import framework_rsa
from ext import conf


def sorted_dict(data):
    sorted_data = sorted(data.items(), key=lambda e: e[0], reverse=False)
    return "&".join(u"{}={}".format(k, v) for k, v in sorted_data)


def cipher_data(data):
    private_key = framework_rsa.read_key(
        conf.config['RSA_PRIVATE_KEY_PATH'], "private")
    cipher_text = framework_rsa.rsa_pkcs1_encrypt(data, private_key)
    return cipher_text


def add_sign(params):
    if params.get('user'):
        data = params
        data['time'] = str(int(time.time()))
        sorted_msg = sorted_dict(data)
        sorted_msg = '{}&w_salt={}'.format(
            sorted_msg, conf.config['SCAN_API_KEY'])
        data['sign'] = SHA.new(sorted_msg.encode('utf-8')).hexdigest().lower()

        msg = "&".join(u"{}={}".format(k, v) for k, v in data.items())
        c_msg = cipher_data(msg)
        return '{}{}'.format(conf.config['QR_CODE_TYPE'], c_msg)

    return ''


def verify_sign(params):
    sign = params.pop('sign', None)
    sort_data = sorted(params.items(), key=lambda e: e[0], reverse=False)
    msg = "&".join(u"{}={}".format(k, v) for k, v in sort_data)
    msg = '{}&w_salt={}'.format(msg, conf.config['SCAN_API_KEY'])
    sha1 = hashlib.sha1()
    sha1.update(msg.encode('gb2312'))
    if sign == sha1.hexdigest().lower():
        return True
    return False
