# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from werkzeug.utils import ImportStringError
from flask import Flask
from werkzeug.utils import find_modules, import_string
from flasgger import Swagger
from flask_cors import *


def register_blueprints(root, app):
    """
    蓝图注册帮助函数

    args:
        root: 蓝图所在模块
        app: Flask实例
    """

    # find_modules读到pyc了,import_string会报错
    for name in find_modules(root, recursive=False):
        try:
            mod = import_string(name)
            if hasattr(mod, 'bp') and hasattr(mod, 'url_prefix'):
                app.register_blueprint(
                    mod.bp, url_prefix=mod.url_prefix)
        except ImportStringError:
            continue


def create_app():
    """
    创建flask app对象
    """

    # app = Flask(__name__)
    #
    # Swagger(app)
    # CORS(app, supports_credentials=True)
    #
    # # 加载配置
    # from config import load_config
    # app.config.from_object(load_config())
    #
    # # 初始化log conf对象
    # from ext import log, conf, cache
    # log.init_app(app)
    # conf.init_app(app)
    # cache.init_app(app)
    #
    # from flask_sqlalchemy import SQLAlchemy
    # SQLAlchemy(app)
    # register_blueprints('controller', app)
    # # from controller import bp
    # # app.register_blueprint(bp, url_prefix='/user')

    app = Flask(__name__)
    Swagger(app)

    CORS(app, supports_credentials=True)

    # 加载配置
    from config import load_config
    app.config.from_object(load_config())

    # 初始化log conf对象
    from ext import log, conf, cache
    log.init_app(app)
    conf.init_app(app)
    cache.init_app(app)
    from flask_sqlalchemy import SQLAlchemy
    SQLAlchemy(app)
    register_blueprints('controller', app)

    return app


"""应用app对象"""
app = create_app()


if __name__ == '__main__':
    # from controller.AdminUserController import bp as admin_user
    # from controller.AdvertController import bp as advert
    # from controller.BillController import bp as bill
    # from controller.BusRouteController import bp as busroute
    # from controller.CallbackController import bp as callback
    # from controller.CarController import bp as car
    # from controller.CertificationController import bp as certification
    # from controller.ClientAppController import bp as clientapp
    # from controller.ClientDeviceController import bp as clientdevice
    # from controller.CompanyController import bp as company
    # from controller.CouponController import bp as coupon
    # from controller.CouponTypeController import bp as coupontype
    # from controller.DeviceController import bp as device
    # from controller.DistrictCodeController import bp as district
    # from controller.FeedbackController import bp as feedback
    # from controller.IdentityController import bp as identity
    # from controller.IndexHomeController import bp as indexhome
    # from controller.LostAndFoundController import bp as lostandfound
    # from controller.MiniController import bp as mini
    # from controller.NoticeController import bp as notice
    # from controller.OrderController import bp as order
    # from controller.PassengerIdentityController import bp as passenger
    # from controller.RechargeController import bp as recharge
    # from controller.RoleController import bp as role
    # from controller.SettlementController import bp as settlement
    # from controller.UserProfileController import bp as userprofile
    #
    # app.register_blueprint(admin_user, url_prefix='/api_backend/v1')
    # app.register_blueprint(advert, url_prefix='/api_backend/v1')
    # app.register_blueprint(bill, url_prefix='/api_backend/v1')
    # app.register_blueprint(busroute, url_prefix='/api_backend/v1')
    # app.register_blueprint(callback, url_prefix='/api_backend/v1')
    # app.register_blueprint(car, url_prefix='/api_backend/v1')
    # app.register_blueprint(certification, url_prefix='/api_backend/v1')
    # app.register_blueprint(clientapp, url_prefix='/api/v1')
    # app.register_blueprint(clientdevice, url_prefix='/api/v1')
    # app.register_blueprint(company, url_prefix='/api_backend/v1')
    # app.register_blueprint(coupon, url_prefix='/api_backend/v1')
    # app.register_blueprint(coupontype, url_prefix='/api_backend/v1')
    # app.register_blueprint(device, url_prefix='/api_backend/v1')
    # app.register_blueprint(district, url_prefix='/api_backend/v1')
    # app.register_blueprint(feedback, url_prefix='/api_backend/v1')
    # app.register_blueprint(identity, url_prefix='/api_backend/v1')
    # app.register_blueprint(indexhome, url_prefix='/api_backend/v1')
    # app.register_blueprint(lostandfound, url_prefix='/api_backend/v1')
    # app.register_blueprint(notice, url_prefix='/api_backend/v1')
    # app.register_blueprint(order, url_prefix='/api_backend/v1')
    # app.register_blueprint(passenger, url_prefix='/api_backend/v1')
    # app.register_blueprint(recharge, url_prefix='/api_backend/v1')
    # app.register_blueprint(role, url_prefix='/api_backend/v1')
    # app.register_blueprint(settlement, url_prefix='/api_backend/v1')
    # app.register_blueprint(userprofile, url_prefix='/api_backend/v1')
    # app.register_blueprint(mini, url_prefix='/api_backend/v1')
    app.run(host='0.0.0.0', port=5001)
