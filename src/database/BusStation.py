# coding:utf-8
from db import db

status_tuple = (
	(1, "启用"),
	(2, "禁用"),
)


class BusStation(db.Model):
	"""公交站点"""

	__tablename__ = 'bus_station'

	id = db.Column(db.BigInteger, primary_key=True)
	name = db.Column(db.String(32))			# 名字(可同名)
	number = db.Column(db.String(32))			# 批次号
	status = db.Column(db.Integer)			# 状态
	longitude = db.Column(db.Numeric(11, 6))	# 经度
	latitude = db.Column(db.Numeric(11, 6))		# 纬度
	company_id = db.Column(db.Integer)			# 所属公司

