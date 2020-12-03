# coding:utf-8
from db import db
from datetime import datetime


class Advert(db.Model):
	"""广告"""
	__tablename__ = 'advert'

	id = db.Column(db.BigInteger, primary_key=True)
	name = db.Column(db.String(30))				# 广告名称
	image = db.Column(db.String(256))			# 广告图链接
	url = db.Column(db.String(200))				# 广告链接
	create_time = db.Column(db.DateTime, default=datetime.now)	# 创建时间
	start_time = db.Column(db.DateTime, default=datetime.now)	# 开始时间
	end_time = db.Column(db.DateTime, default=datetime.now)		# 结束时间
	is_active = db.Column(db.Integer)							# 是否上线
	adv_location = db.Column(db.Integer)		# 展示位置 1首页 2弹出框 3首次开启
	company_id = db.Column(db.Integer)
