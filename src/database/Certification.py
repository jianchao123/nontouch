# coding:utf-8
from db import db
from datetime import datetime

STATUS_TUPLE = (
	(1, "审核中"),
	(2, "审核通过"),
	(3, "审核失败"),
	(4, "APP端隐藏")
)


class Certification(db.Model):
	"""乘客身份认证记录"""
	__tablename__ = 'certification'

	id = db.Column(db.BigInteger, primary_key=True)
	upload_imgs = db.Column(db.String(256))			# 上传的图片
	status = db.Column(db.Integer)					# 状态
	date_of_approval = db.Column(db.DateTime, default=datetime.now)	# 审核时间
	pass_reason = db.Column(db.String(128))			# 通过原因
	company_id = db.Column(db.Integer)				# 审核的公司
	identity_id = db.Column(db.Integer)				# 身份
	user_id = db.Column(db.Integer)					# 乘客
	verifier_id = db.Column(db.Integer)				# 审核人
