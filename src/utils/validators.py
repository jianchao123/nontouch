# coding:utf-8
import re


def mobile_validate(mobile):
    ret = re.match(r"^1[345678]\d{9}$", mobile)
    if ret:
        return True
    return False

