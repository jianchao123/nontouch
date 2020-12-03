# coding:utf-8
from db import db


class UserPermissions(db.Model):
	"""用户权限"""
	__tablename__ = 'user_permissions'

	id = db.Column(db.BigInteger, primary_key=True)
	permission_id = db.Column(db.Integer)	# 权限id
	user_id = db.Column(db.Integer)			# 后台用户id
	company_id = db.Column(db.Integer)
