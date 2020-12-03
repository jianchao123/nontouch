# coding:utf-8
from db import db
from datetime import datetime


class Notice(db.Model):
	"""公告"""
	__tablename__ = 'notice'

	id = db.Column(db.BigInteger, primary_key=True)
	name = db.Column(db.String(30))				# 公告标题
	content = db.Column(db.String(200))			# 公告内容
	create_time = db.Column(db.DateTime, default=datetime.now)	# 公告创建时间
	start_time = db.Column(db.DateTime, default=datetime.now)	# 公告开始时间
	end_time = db.Column(db.DateTime, default=datetime.now)		# 公告结束时间
	priority = db.Column(db.Integer)					# 公告优先级
	is_active = db.Column(db.Integer)					# 公告是否上线
	company_id = db.Column(db.Integer)
