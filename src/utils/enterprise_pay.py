# coding:utf-8
import ujson
import OpenSSL
from datetime import datetime
import hashlib
import textwrap
import base64
import requests
import json
from alipay.aop.api.util.SignatureUtils import *


class test():

    rsaPrivateKey = 'MIIEowIBAAKCAQEAjpMriEdc+pwRLgPhwWENPfnVpMQn96B3cKla6OPc9a0qF5PpBQJu8CQkip0jvN6vDPOMB35/zeDH8gp6XkQBv0P69H+nYy3qKWfgCWMPMPW4hm3GcnEv+fp41uxsWP8riEoaOCKqNz+bOanTygfrL3u+5SiYTHOYmh0dXcnG1d3zlFH97kpIxjD/kheD2Twltm/3E3Mh5eliSngr+6Wms19CGI4pkbkNy22f8EpH+/yNirij0emuKyCBDM1AIVfUgH67Iz5Hm/7IPzW4ueZzV14hrOrxExGbhooY3tV8fN9yvIPM2gGWnISgi0gOsM0/fpD/NYoY1UpaXhPXu5jyiQIDAQABAoIBAB8z+FgH/kJeu6fNc7AF1IcW0XoQ8ApS1TET73B+xhIChu7IETxmbu8hidnIUFT6i2cTOjc9qSzeoAPJ5UQSMCuy7g5qjbC4EMJlGHQVePKnJG5PQhozyWM1PRMUhRXpKpbWWOymMYiL5CX3lAFoQEGRHJM8kjBRMDmyW4X2Lg0KBagyzdfsGxvwanS2WRquLOhQ7IhOa5LGSR1dBKKuoUj+z06x0pE+cf+1YAKh797vKW5hylx0QjfIWOgKC9iH+Ft7nPc9LG6k5DL4Gc0hzJXqGeEairzj45s1sIbN+SMf8uhBtI/ciBqGoU6ZsChHjPuqrR39QCeGiMjfbdtNbgECgYEAxGEXYV4fkbVgldZe3yNM5gKGo6tutSITPChW/maW8QtuvlVTX200KAn/oDFbmYCq460aJGmZz45GT95OOpXlX2p42TvtWwKXYIFsS9GPvv6d8d4KlevKxVShRB0QPCPbephtLiiEQ0rtJpjf2F9aTAH13ggu7WhUedmcJ37c0kECgYEAudxRFP3K9S1qcBpW2up1HpE8JSy+VhN/Hzt0QzO5qZRN9rKOkMI+1ovFSGgZxssniOPTkM4pcqEEzUbueCOgRrm/RBu3c5KCN2R3ynJwaUgDtgZOW9eAOnc1rFtrMHFpq0gvTrjlHVylBrsvIyG1roQ7u83XtqEnogXY0wvlfkkCgYEAqajoNirHQ29cHpeyJz2sNhuAju6RGtRxocuIPQoM5ftmlfHJsev634yj2JZL+PZ8rW7j4wmI5RSaEm6RT3QpUqH9/lAT5Ej811d5ZJeMhQodEtUueA/ag1l2ag5h9FNWTzhZO0Ot4SVedbYlzh2zOW+IJ2cSg/Fa6lri2gx0YwECgYA2F9s5YswpI3iw+9l/iXFg3iBFKYqT/sSm0GT8EhfdNR6jyEAZ/Y7QXomikzm9U+9DthsjL/18MUT2gchyCtxg+TqjlfWEm4Vunb0HnNr+qUj7N0ajEEtvuLZUXZ8K0FdS1IWAQevc6dPV67DCZtM74ZyJAlXf/3NLgqwicHnwkQKBgDHbGMUZPUOgw9REcm0ZGepZOK/Synw0qvX+oUzYAvPD1BYBwmhK3eOYBrLtamsu/9S/5S2T0h1BY6nHv/E/mk8Xqx3Dy0W7oFOzbjVDIRFWVK9jq6xoWGHv9YcXM+WoZJWpGDqKkPJvKR1WZ1mjhLDJVNObxklYBeukBNjDMDgz'

    def __init__(self, app_id='2021002127658564'):
        self.gatewayUrl = 'https://openapi.alipay.com/gateway.do'
        self.method = 'alipay.fund.trans.uni.transfer'
        self.appId = app_id
        self.apiVersion = '1.0'
        self.signType = 'RSA2'
        self.postCharset = 'UTF-8'
        self.format = 'json'
        self.apiVersion = '1.0'
        #self.appCertSN = self.getCertSN('/home/jianchao/code/nontouch_1/doc/credential/appCertPublicKey_2021002127658564.crt')
        #self.alipayRootCertSN = self.getRootCertSN('/home/jianchao/code/nontouch_1/doc/credential/alipayRootCert.crt')

    def getCertSN(self, path):
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, open(path).read())
        certIssue = cert.get_issuer()
        issuer_info = []
        for key, val in dict(certIssue.get_components()).items():
            issuer_info.insert(0, (key.decode(), val.decode()))

        sn = hashlib.md5('{}{}'.format(self.array2string(dict(issuer_info)), cert.get_serial_number()).encode()).hexdigest()
        return sn

    def getRootCertSN(self, path):
        cert_content = open(path).read()
        cert_list = cert_content.split("-----END CERTIFICATE-----")
        sn = None
        for cert in cert_list:
            if cert:
                cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, "{}-----END CERTIFICATE-----".format(cert))
                serial_number = str(cert.get_serial_number())
                if serial_number.find('0x') == 0:
                    serial_number = int(serial_number, 16)
                if cert.get_signature_algorithm().decode('utf-8') in ['sha256WithRSAEncryption', 'sha1WithRSAEncryption']:
                    certIssue = cert.get_issuer()
                    issuer_info = []
                    for key, val in dict(certIssue.get_components()).items():
                        issuer_info.insert(0, (key.decode(), val.decode()))

                    if not sn:
                        sn = hashlib.md5('{}{}'.format(self.array2string(dict(issuer_info)), serial_number).encode()).hexdigest()
                    else:
                        sn += "_{}".format(hashlib.md5('{}{}'.format(self.array2string(dict(issuer_info)), serial_number).encode()).hexdigest())
        return sn

    def array2string(self, params):
        string = []
        if params and isinstance(params, dict):
            for key, val in params.items():
                string.append("{}={}".format(key, val))
        return ','.join(string)

    def transfer(self, order):
        biz_content = ujson.dumps(order)

        params = {
            'app_id': self.appId,
            'version': self.apiVersion,
            'format': self.format,
            'sign_type': self.signType,
            'charset': self.postCharset,
            'method': self.method,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'biz_content': biz_content,
            'app_cert_sn': 'f6b8233ca7ca50311154f5a5f9c5ab7b', #self.appCertSN,
            'alipay_root_cert_sn': '687b59193f3f462dd5336e5abf83c5d8_02941eef3187dddf3d3b83462e1dfcf6' #self.alipayRootCertSN
        }
# "alipay_root_cert_sn,app_cert_sn,app_id,biz_content,charset,format,method,sign_type,timestamp,version"
        params['sign'] = self.sign(params, self.signType)
        res = self.send_request_data(self.gatewayUrl, params)
        print(res.content)

    def send_request_data(self, url, params):
        kv_list = []
        for k, v in params.items():
            kv_list.append(k + "=" + v)

        return requests.get(url + "?" + "&".join(kv_list))

    def sign(self, data, signType='RSA2'):
        content = get_sign_content(data)
        res = "-----BEGIN RSA PRIVATE KEY-----\n{}\n-----END RSA PRIVATE KEY-----".format('\n'.join(textwrap.wrap(self.rsaPrivateKey, 64)))

        if not res:
            raise ValueError('Error: {}'.format('您使用的私钥格式错误，请检查RSA私钥配置'))

        if signType == 'RSA2':
            sign = self.openssl_sign(content, res, 'sha256')
        else:
            sign = self.openssl_sign(content, res)

        return sign

    def openssl_sign(self, content, priv_key_id, signature_alg='sha1'):
        """
        生成签名
        :param content:
        :return:
        """
        if not content or not priv_key_id:
            return False
        pkey = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, priv_key_id)
        if pkey:
            signature = OpenSSL.crypto.sign(pkey, content.encode('utf8'), signature_alg)
            ret = base64.b64encode(signature)
            return ret.decode('utf8').replace('\n', '')
        return False

    def alipay_sign(self, data_dict):

        __pem_begin = '-----BEGIN RSA PRIVATE KEY-----\n'
        __pem_end = '\n-----END RSA PRIVATE KEY-----'

        def rsa_sign(data_dict, private_key_path):
            """SHAWithRSA

            :param content: 签名内容
            :type content: str

            :param private_key: 私钥
            :type private_key: str

            :param _hash: hash算法，如：SHA-1,SHA-256
            :type _hash: str

            :return: 签名内容
            :rtype: str
            """

            private_key = _format_private_key(
                open(private_key_path, 'r').read())
            pri_key = rsa.PrivateKey.load_pkcs1(private_key.encode('utf-8'))
            params_list = sorted(data_dict.items(), key=lambda e: e[0],
                                 reverse=False)  # 参数字典倒排序为列表
            print params_list
            params_str = "&".join(
                u"{}={}".format(k, v) for k, v in params_list)  # 待签名字符串
            print params_str
            sign_result = rsa.sign(params_str.encode('utf-8'), pri_key,
                                   'SHA-256')
            return base64.b64encode(sign_result)

        def _format_private_key(private_key):
            """对私进行格式化，缺少"-----BEGIN RSA PRIVATE KEY-----"和"-----END RSA PRIVATE KEY-----"部分需要加上

            :param private_key: 私钥
            :return: pem私钥字符串
            :rtype: str
            """
            if not private_key.startswith(__pem_begin):
                private_key = __pem_begin + private_key
            if not private_key.endswith(__pem_end):
                private_key = private_key + __pem_end
            return private_key

        sign = rsa_sign(data_dict, '/home/jianchao/code/nontouch_1/doc/credential/wgxing.com_私钥.txt')

        return sign


test_class = test()
test_class.transfer({
            'out_biz_no': str(datetime.now().strftime('%Y%m%d%H%M%S%f')),
            'trans_amount': '0.1',
            'product_code': 'TRANS_ACCOUNT_NO_PWD',
            'biz_scene': 'DIRECT_TRANSFER',
            'order_title': '测试转账',
            'payee_info': {
                'identity_type': 'ALIPAY_LOGON_ID',
                'identity': '18508217537',
                'name': '简超'
            },
            'remark': '测试转账'
        })





