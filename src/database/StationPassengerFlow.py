# coding:utf-8
from db import db


class StationPassengerFlow(db.Model):
	"""站点客流"""
	__tablename__ = 'station_passenger_flow'

	id = db.Column(db.BigInteger, primary_key=True)
	number = db.Column(db.Integer)	# 客流数量
	station_id = db.Column(db.Integer)	# 站点
	company_id = db.Column(db.Integer)