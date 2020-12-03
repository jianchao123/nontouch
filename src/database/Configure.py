# coding:utf-8
from db import db


class Configure(db.Model):
	"""配置"""
	__tablename__ = 'configure'

	id = db.Column(db.BigInteger, primary_key=True)
	key = db.Column(db.String(16))		# KEY
	value = db.Column(db.String(1024))	# VALUE
