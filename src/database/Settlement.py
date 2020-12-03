# coding:utf-8
from db import db
from datetime import datetime


class Settlement(db.Model):
	"""结算"""
	__tablename__ = 'settlement'

	id = db.Column(db.BigInteger, primary_key=True)
	create_time = db.Column(db.DateTime, default=datetime.now)
	start_time = db.Column(db.DateTime, default=datetime.now)	# 开始时间
	end_time = db.Column(db.DateTime, default=datetime.now)		# 结束时间
	status = db.Column(db.Integer)								# 订单支付状态 1结算完成 2已打款
	amount = db.Column(db.Numeric(11, 6))						# 结算总金额
	xls_oss_url = db.Column(db.String(128))							# oss url
	company_id = db.Column(db.Integer)							# 公司
