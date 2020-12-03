# coding:utf-8
from db import db
from datetime import datetime

VERIFY_TYPE_CHOICES = ((1, '无感行二维码'), (2, '人脸'), (3, 'IC卡'), (4, '现金'),
                       (5, '微信'), (6, '支付宝'), (7, '银联'))
DISCOUNT_WAY_CHOICES = ((0, '无优惠'), (1, '身份'), (2, '优惠券'), (3, '免费'))


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.BigInteger, primary_key=True)
    order_no = db.Column(db.Integer)                            # 订单号
    create_time = db.Column(db.DateTime, default=datetime.now)
    pay_time = db.Column(db.DateTime, default=datetime.now)     # 订单支付时间
    bus_id = db.Column(db.String(10))                           # 汽车车牌号
    scan_time = db.Column(db.DateTime, default=datetime.now)    # 扫码时间
    amount = db.Column(db.Numeric(11, 6))                       # 乘车金额
    discount = db.Column(db.Numeric(11, 6))                     # 折扣金额
    real_amount = db.Column(db.Numeric(11, 6))                  # 实付金额
    discount_way = db.Column(db.Integer)                        # 折扣方式 0.无优惠 1.身份 2.优惠券 3.免费
    device_no = db.Column(db.String(32))                        # 设备号
    up_stamp = db.Column(db.DateTime, default=datetime.now)     # 订单上送时间
    verify_type = db.Column(db.Integer)                         # 验证方式
    sub_account = db.Column(db.String(32))                      # 子账户
    content = db.Column(db.String(128))                         # 相关内容
    company_id = db.Column(db.Integer)                          # 公司
    route_id = db.Column(db.Integer)                            # 线路
    pay_type = db.Column(db.Integer)                            # 支付方式 1支付宝 2微信 3银联 4余额
    status = db.Column(db.Integer)                              # 订单状态 1待支付 2成功 3失败
    station_id = db.Column(db.Integer)                          # 上车站点
    user_id = db.Column(db.Integer)                             # 用户id
