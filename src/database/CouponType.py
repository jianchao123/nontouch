# coding:utf-8
from db import db
from datetime import datetime

type_tuple = ((1, "抵扣金额"),)
status_tuple = ((1, "未开始"), (2, "活动中"), (3, "活动结束"), (10, "删除"))
condition_tuple = (
	(1, "全部用户"),
	(2, "新注册用户"),
	(3, "分享送券"),
)


class CouponType(db.Model):
	"""优惠券类型"""
	__tablename__ = 'coupon_type'

	id = db.Column(db.BigInteger, primary_key=True)
	name = db.Column(db.String(32))							# 名称
	give_out_begin_time = db.Column(db.DateTime, default=datetime.now)	# 分发开始时间
	give_out_end_time = db.Column(db.DateTime, default=datetime.now)	# 分发截止时间
	use_begin_time = db.Column(db.DateTime, default=datetime.now)		# 使用开始时间
	use_end_time = db.Column(db.DateTime, default=datetime.now)			# 使用截止时间
	volume = db.Column(db.Integer)					# 发放总量
	residue_volume = db.Column(db.Integer)			# 当前余量
	has_been_used_volume = db.Column(db.Integer)	# 已使用量
	type = db.Column(db.Integer)
	face_value = db.Column(db.Numeric(11, 6))		# 面值
	img_url = db.Column(db.String(128))				# 优惠券图片
	content = db.Column(db.String(32))
	link = db.Column(db.String(128))				# 优惠券活动链接
	condition = db.Column(db.Integer)				# 领取优惠券的条件
	status = db.Column(db.Integer)
	is_online = db.Column(db.Integer)				# 是否上线
	create_time = db.Column(db.DateTime, default=datetime.now)
	company_id = db.Column(db.Integer)				# owner_id
