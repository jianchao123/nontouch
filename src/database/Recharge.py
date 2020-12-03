# coding:utf-8
from db import db
from datetime import datetime


class Recharge(db.Model):
	"""充值记录"""
	__tablename__ = 'recharge'

	id = db.Column(db.BigInteger, primary_key=True)
	order_no = db.Column(db.String(64))			# 订单编号
	create_time = db.Column(db.DateTime, default=datetime.now)
	pay_time = db.Column(db.DateTime, default=datetime.now)	# 支付时间
	name = db.Column(db.String(30))			# 商品名称
	body = db.Column(db.String(100))		# 商品描述
	amount = db.Column(db.Numeric(11, 6))	# 金额
	remark = db.Column(db.String(30))		# 支付失败原因
	trade_no = db.Column(db.String(64))		# 支付宝交易凭证号
	to_whom = db.Column(db.String(11))		# 代充手机号
	pay_type = db.Column(db.Integer)		# 支付方式(1-支付宝 2-微信 3-银联)
	status = db.Column(db.Integer)			# 订单状态(1:待支付,2:成功,3:失败)
	user_id = db.Column(db.Integer)
	company_id = db.Column(db.Integer)		# owner_id