# coding:utf-8
from db import db
from datetime import datetime
status_tuple = ((1, u"启用中"), (2, u"禁用中"))


class Company(db.Model):
	"""公司"""
	__tablename__ = 'company'

	id = db.Column(db.BigInteger, primary_key=True)
	name = db.Column(db.String(30))			# 公司名称
	house_number = db.Column(db.String(64))	# 门牌号
	permissions = db.Column(db.Text())		# 该公司所有的权限
	status = db.Column(db.Integer)
	create_time = db.Column(db.DateTime, default=datetime.now)
	line_nos = db.Column(db.String(128))	# 公交公司所有的线路(逗号分割),用于初始化
	logo = db.Column(db.String(128))
	domain = db.Column(db.String(128))		# 域名
	admin_user_id = db.Column(db.Integer)	# 管理员帐号
	area_id = db.Column(db.Integer)			# 区
	city_id = db.Column(db.Integer)			# 市
	province_id = db.Column(db.Integer)		# 省
	level = db.Column(db.Integer)			# 等级 1-五感行 2-其他公交公司 3-其他公交
	parent_id = db.Column(db.Integer)		# 父级公司
	company_id = db.Column(db.Integer)		# 所属公司
