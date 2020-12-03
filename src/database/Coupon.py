# coding:utf-8
from db import db
from datetime import datetime

status_tuple = (
	(1, "未发放"),
	(2, "已发放"),
	(3, "已使用"),
	(4, "已过期")	# 只有已经发放了才能过期
)


class Coupon(db.Model):
	"""优惠券"""
	__tablename__ = 'coupon'

	id = db.Column(db.BigInteger, primary_key=True)
	code = db.Column(db.String(32))				# 券码
	face_value = db.Column(db.Numeric(11, 6))	# 面值
	status = db.Column(db.Integer)
	use_begin_time = db.Column(db.DateTime, default=datetime.now)	# 使用开始时间
	use_end_time = db.Column(db.DateTime, default=datetime.now)		# 使用截止时间
	type_id = db.Column(db.Integer)				# 优惠券类型
	company_id = db.Column(db.Integer)
