# coding:utf-8
from db import db
from datetime import datetime


class Feedback(db.Model):
	"""反馈"""
	__tablename__ = 'feedback'

	id = db.Column(db.BigInteger, primary_key=True)
	content = db.Column(db.Text())		# 反馈内容
	start_time = db.Column(db.DateTime, default=datetime.now)	# 反馈时间
	end_time = db.Column(db.DateTime, default=datetime.now)		# 解决时间
	remarks = db.Column(db.Text())		# 反馈备注
	type_id = db.Column(db.String(32))		# 关联反馈来源
	user_id = db.Column(db.Integer)		# 关联反馈的用户
	company_id = db.Column(db.Integer)
