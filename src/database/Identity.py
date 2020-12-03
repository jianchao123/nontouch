# coding:utf-8
from db import db
from datetime import datetime

STATUS_TUPLE = (
	(1, "使用中"),
	(10, "已删除")
)


class Identity(db.Model):
	"""乘客身份"""
	__tablename__ = 'identity'

	id = db.Column(db.BigInteger, primary_key=True)
	name = db.Column(db.String(16))					# 身份名称
	description = db.Column(db.String(128))			# 描述
	discount_rate = db.Column(db.Numeric(11, 6))	# 折扣比率
	status = db.Column(db.Integer)
	months = db.Column(db.Integer)					# 月数
	number = db.Column(db.Integer)					# 次数
	create_time = db.Column(db.DateTime, default=datetime.now)
	company_id = db.Column(db.Integer)				# 所属公司
