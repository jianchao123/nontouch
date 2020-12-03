# coding:utf-8

try:
    import os
    from default import Config
    from development import DevelopmentConfig
    from production import ProductionConfig
    from testing import TestingConfig
except:
    import traceback
    print traceback.format_exc()


def load_config():
    """
    根据环境变量的值读取配置
    """
    try:
        mode = os.environ.get("NONTOUCH_1_ENV")
        print "-------------------{}".format(mode)
        if mode == 'PRO':
            return ProductionConfig
        elif mode == 'TEST':
            return TestingConfig
        else:
            return DevelopmentConfig
    except ImportError:
        return Config
