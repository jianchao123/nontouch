# coding:utf-8
from db import db


class PassengerWeeklyCount(db.Model):
	"""用户每周每条线乘坐次数(只记录次数前3的乘坐线路)
	删除子账户需要删除此表记录
	"""
	__tablename__ = 'passenger_weekly_count'

	id = db.Column(db.BigInteger, primary_key=True)
	mobile = db.Column(db.String(32))	# 手机号
	count = db.Column(db.Integer)		# 线路
	route_id = db.Column(db.Integer)	# 次数
	company_id = db.Column(db.Integer)
