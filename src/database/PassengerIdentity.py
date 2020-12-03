# coding:utf-8
from db import db
from datetime import datetime
STATUS_TUPLE = (
	(1, "生效中"),
	(2, "已过期"),
	(10, "已删除")
)


class PassengerIdentity(db.Model):
	"""乘客身份"""
	__tablename__ = 'passenger_identity'

	id = db.Column(db.BigInteger, primary_key=True)
	identity_name = db.Column(db.String(16))		# 身份卡名字
	status = db.Column(db.Integer)
	discount_rate = db.Column(db.Numeric(11, 6))	# 折扣比率
	end_time = db.Column(db.DateTime, default=datetime.now)	# 身份截止时间
	section_begin_time = db.Column(db.DateTime, default=datetime.now)	# 区间次数开始时间
	section_end_time = db.Column(db.DateTime, default=datetime.now)		# 区间次数结束时间
	residue_number = db.Column(db.Integer)			# 剩余免费次数
	certification_id = db.Column(db.Integer)		# 关联的审核
	company_id = db.Column(db.Integer)				# 公司
	identity_id = db.Column(db.Integer)				# 身份
	user_id = db.Column(db.Integer)					# 乘客
