# coding:utf-8
from db import db
from datetime import datetime
status_tuple = (
	(1, "有效"),
	(2, "删除"),
)


class Roles(db.Model):
	"""角色表"""
	__tablename__ = 'roles'

	id = db.Column(db.BigInteger, primary_key=True)
	role_name = db.Column(db.String(16))		# 角色名字
	show_name = db.Column(db.String(16))		# 显示名字
	describe = db.Column(db.String(32))			# 描述
	create_time = db.Column(db.DateTime, default=datetime.now)
	status = db.Column(db.Integer)
	company_id = db.Column(db.Integer)			# 所属公司
