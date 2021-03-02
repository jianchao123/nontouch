# coding:utf-8
import OpenSSL
from datetime import datetime
import hashlib
import urllib
import json
import base64
import requests
from alipay.aop.api.util.SignatureUtils import *


class test():

    rsaPrivateKey = 'MIIEogIBAAKCAQEAhnoMJfypnKSbU1ngv68UsLxpq4kxz048eeeljgevcx9WQoHg/LBnGN5peqeohVMnlyMDNk77XHeZPh1Sf0I24rlZZJFRsJ8HAUtDM4cDsdSH7bZ7VNpzMW4bTSUFp2gpbb9Ch/F0PYkkRpkxwKsv/qptaoe4GuRE+cGEu2sDvAskTckb4bfkX1Be0GZFPSZyjwu9lqFqdCazY7N06MAG40OSa2DPMAnxv2Mc6O42HfdxsDpQeVV6wfqGVsGPr9W5eZqkOOSpS2wYStmNa5Uhm2OCnLOzEp5uRtrLtCkigrBBdit9/ox8ezDNvF3XDDuEEmkjfy0GiTr88uvHC4ta/wIDAQABAoIBAG+ms6Fyhyycaq4oqHbeGbKnrKCUdzukvIeGcilbbiuKMCdmCHQkzmSSfUcuHrgbk3pjwo37w61BS4WL+OvaARH7TCI4mXeogbtsTq5gggvK5tTSNtH70bqPrbE+dNRKomMRcl7GdXmF/Q10sh9CwsWRoOjbKFuDfVVUfCzTrDUaYsTtBjnwvKXqNItirUHtjWfHUmGXWMkikTwCY8xt/B0CGuZznGbr/JDAZZh9R7u07+oRJ3Y4SGkXMrDgvB9Ls6cOytF0sNtMavsM2HeDaF0iNL1+ekFgSUBKLBBmOojbBJvPkWUV+gw9nHcntTIrG4VbReRoSTt0+7mdWJqn1NECgYEAwMYwZhh4bghei+5ulGgFuGNVcd8IUKufZO9KAkrLDMHRgbWVm0omRjixFd/vIflgSscbJEJ32CYjdn9RdJ59LQa5eNPjF8cm+kJ2AM9OufQ25yT+xh2lmUPC0+01XXtDot2tt5yV2r4SqpZSux42s7xG7tibartVwxsHic3OCtcCgYEAspUOzH8EMsfrsPkD3kvlSSbIZOvFOFyqZI9HIJ5fOg3h1PnU4Y/ue+V7e8xhgYFNz7GdXa7fCMQfwsXGNR9gVdKryjdzx5fdMBn+sOCznMDJ+jMGkYZ81J06mkbdIqc+CRfnnLlCKU4pjWu4VPm8p1ivP5mictm+5TrqvrAYlBkCgYASt2tdjkSrEj7zwRuVZyAfDe3u12O8SV15dE4wOMjMHUlVGadD44ghy0FOSWazWr4BpKE6/QUbxGAvEh97fiPTKlL5q0DiPyDGrYs9euM+5Lor6QiffaNlZRHWd7J1uBESEAncyOQ3z7qKO3we1Mkk3EPazscQLs4d2lL6CzRVEwKBgDOIkByzCqMczgbj1RnxDNlvN6Tn5KG/G+yo6/2dth0qpGCxN51fy5I1Rs0SzZBxn+KvfpnqPLJq5j9ukyQBSet6P9i6585RJKMc3UJtlWdGuwJYdyzHgn5YYPDkQiwd1ukI3O19CHqi85q72xWqe6ZPEUNpMleyPkQoHFWqu20BAoGAH+4vzq77ENGImTFI33t3VIXU2w4i44zksJUqR7vDzy/lOly6mDYkq/jM4JBByxvJ1uuF5k4EYYacLdW/A/IqbB6PPci8AVyIiHNhcVkk3xyAWjy5jOiQgtvCZIxbW6rFG84qiFw2gi3H7e1z74rItoLsvenrfhtZRSy1FdwkxwU='

    def __init__(self, app_id='2021002127658564'):
        self.gatewayUrl = 'https://openapi.alipay.com/gateway.do'
        self.method = 'alipay.fund.trans.uni.transfer'
        self.appId = app_id
        self.apiVersion = '1.0'
        self.signType = 'RSA2'
        self.postCharset = 'UTF-8'
        self.format = 'json'
        self.apiVersion = '1.0'

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
        return '&'.join(string)

    def transfer(self, order):
        biz_content = json.dumps(order)

        params = {
            'app_id': self.appId,
            'version': self.apiVersion,
            'format': self.format,
            'sign_type': self.signType,
            'charset': self.postCharset,
            'method': self.method,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'biz_content': biz_content,
            'app_cert_sn': '8975ff37f6bdc0a9a80c1f74987ef3b9', #self.appCertSN,
            'alipay_root_cert_sn': '687b59193f3f462dd5336e5abf83c5d8_02941eef3187dddf3d3b83462e1dfcf6' #self.alipayRootCertSN
        }
        params = order_dict(params)
        print "待签名字符串", self.array2string(params)
        params['sign'] = sign_with_rsa2(self.rsaPrivateKey, json.dumps(params), "utf8")
        print "签名串", urllib.quote(params['sign'])
        res = self.send_data(self.gatewayUrl, params)
        print(res.content)

    def send_data(self, url, params):

        kv_list = []
        for k, v in params.items():
            kv_list.append(k + "=" + v)
        u = url + "?" + "&".join(kv_list)
        print u
        return requests.get(u)


def order_dict(d):
    from collections import OrderedDict
    d2 = OrderedDict()
    for row in sorted(d.keys(), reverse=False):
        d2[row] = d[row]
    return d2


test_class = test()

p = {
    'out_biz_no': str(datetime.now().strftime('%Y%m%d%H%M%S%f')),
    'trans_amount': '0.1',
    'product_code': 'TRANS_ACCOUNT_NO_PWD',
    'biz_scene': 'DIRECT_TRANSFER',
    'order_title': '测试转账',
    'payee_info': order_dict({
        'name': '简超',
        'identity_type': 'ALIPAY_LOGON_ID',
        'identity': '18508217537'
    }),
    'remark': '测试转账'
}
data = order_dict(p)
test_class.transfer(data)





