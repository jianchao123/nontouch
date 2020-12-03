# coding:utf-8
from db import db


class UserRole(db.Model):
	"""用户角色"""
	__tablename__ = 'user_role'

	id = db.Column(db.BigInteger, primary_key=True)
	role_id = db.Column(db.Integer)		# 角色id
	user_id = db.Column(db.Integer)		# 用户id
	company_id = db.Column(db.Integer)
