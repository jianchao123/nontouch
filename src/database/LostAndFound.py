# coding:utf-8
from db import db
from datetime import datetime

status_tuple = ((1, "未认领"), (2, "已认领"), (10, "删除"))


class LostAndFound(db.Model):
	"""失物招领"""
	__tablename__ = 'lost_and_found'

	id = db.Column(db.BigInteger, primary_key=True)
	description = db.Column(db.String(128))				# 描述
	city = db.Column(db.String(32))						# 城市
	line_no = db.Column(db.String(32))					# 线路
	contacts = db.Column(db.String(16))					# 联系方式
	status = db.Column(db.Integer)
	create_time = db.Column(db.DateTime, default=datetime.now)
	imgs = db.Column(db.Text())							#
	is_admin_publish = db.Column(db.Integer)	# 是否管理员发布
	create_user_id = db.Column(db.Integer)		# 创建者
	company_id = db.Column(db.Integer)
