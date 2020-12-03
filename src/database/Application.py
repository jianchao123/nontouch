# coding:utf-8
from db import db


class Application(db.Model):
	"""APP"""
	__tablename__ = 'application'

	id = db.Column(db.BigInteger, primary_key=True)
	name = db.Column(db.String(30))			# 名称
	update_content = db.Column(db.Text())	# 应用名称
	version = db.Column(db.String(10))		# 应用版本
	version_code = db.Column(db.Integer)	# 应用版本号
	update_force = db.Column(db.Integer)	# 是否强制更新
	url = db.Column(db.String(128))			# apk链接
