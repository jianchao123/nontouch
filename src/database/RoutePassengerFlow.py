# coding:utf-8
from db import db


class RoutePassengerFlow(db.Model):
	"""线路客流"""
	__tablename__ = 'route_passenger_flow'

	id = db.Column(db.BigInteger, primary_key=True)
	number = db.Column(db.Integer)		# 线路
	route_id = db.Column(db.Integer)	# 客流数量
	company_id = db.Column(db.Integer)