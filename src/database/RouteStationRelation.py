# coding:utf-8
from db import db


class RouteStationRelation(db.Model):
	"""线路站点关系"""
	__tablename__ = 'route_station_relation'

	id = db.Column(db.BigInteger, primary_key=True)
	code = db.Column(db.Integer)			# 线路上的编号
	round_trip = db.Column(db.Integer)		# 往返
	bus_route_id = db.Column(db.Integer)	# 线路id
	bus_station_id = db.Column(db.Integer)	# 站点Id
	company_id = db.Column(db.Integer)