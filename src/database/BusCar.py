# coding:utf-8
from db import db

status_tuple = (
	(1, u'未绑线'),
	(2, u'已绑线'),
	(10, u'删除')
)


class BusCar(db.Model):
	"""公交车"""
	__tablename__ = 'bus_car'

	id = db.Column(db.BigInteger, primary_key=True)
	bus_id = db.Column(db.String(32))		# 车牌号
	brand = db.Column(db.String(16))		# 品牌
	type = db.Column(db.String(16))			# 类型
	model_number = db.Column(db.String(16))	# 型号
	engine = db.Column(db.String(16))		# 引擎
	chassis = db.Column(db.String(16))		# 底盘
	load = db.Column(db.String(16))			# 载重
	bus_load = db.Column(db.String(16))		# 载客量
	product_date = db.Column(db.Date)		# 生产日期
	buy_date = db.Column(db.Date)			# 购买日期
	status = db.Column(db.Integer)			# 状态
	company_id = db.Column(db.Integer)		# 所属公司
	route_id = db.Column(db.Integer)		# 线路id
	is_servicing = db.Column(db.Integer)	# 是否营运中


