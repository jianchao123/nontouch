# coding:utf-8
from db import db

type_tuple = (
	(1, u"扫码设备"),
	(2, u"人脸设备"),
	(3, u"刷卡"),
	(4, u"刷卡扫码二合一"),
)
status_tuple = (
	(1, u"未分配"),
	(2, u"已分配,未绑车"),
	(3, u"已绑车"),
	(10, u"删除")
)


class Device(db.Model):
	"""设备"""

	__tablename__ = 'device'

	id = db.Column(db.BigInteger, primary_key=True)
	name = db.Column(db.String(32))				# 设备名称
	brand = db.Column(db.String(16))			# 品牌
	type = db.Column(db.String(16))				# 设备支付类型
	status = db.Column(db.Integer)
	model_number = db.Column(db.String(16))		# 型号
	pro_seq_number = db.Column(db.String(32))	# 生产序号
	device_no = db.Column(db.String(32))		# 设备号
	manufacture_date = db.Column(db.Date)		# 生产日期
	buy_date = db.Column(db.Date)				# 购买日期
	company_id = db.Column(db.Integer)			# 所属公司
	car_id = db.Column(db.Integer)				# 绑定的车辆
	is_online = db.Column(db.Integer)			# 是否在线
