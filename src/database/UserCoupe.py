# coding:utf-8
from db import db
from datetime import datetime


class UserCoupe(db.Model):
	"""用户优惠券"""
	__tablename__ = 'user_coupe'

	id = db.Column(db.BigInteger, primary_key=True)
	get_time = db.Column(db.DateTime, default=datetime.now)	# 获取时间
	use_time = db.Column(db.DateTime, default=datetime.now)	# 使用时间
	coupon_id = db.Column(db.Integer)	# 优惠券id
	user_id = db.Column(db.Integer)		# 用户id
	company_id = db.Column(db.Integer)