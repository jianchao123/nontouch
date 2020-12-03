# coding:utf-8
from db import db


class Permissions(db.Model):
	"""权限"""
	__tablename__ = 'permissions'

	id = db.Column(db.BigInteger, primary_key=True)
	permission_name = db.Column(db.String(16))	# 权限名字
	entity_classes = db.Column(db.String(32))	# url
	method = db.Column(db.String(32))	# 方法
	group = db.Column(db.String(32))	# 分组
	is_show = db.Column(db.Integer)		# 是否展示这个权限
	is_default = db.Column(db.Integer)	# 是否将这个权限默认给用户
	url = db.Column(db.String(64))
