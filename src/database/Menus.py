# coding:utf-8
from db import db
level_tuple = (
	(1, "一级菜单"),
	(2, "二级菜单"),
)


class Menus(db.Model):
	"""菜单"""
	__tablename__ = 'menus'

	id = db.Column(db.BigInteger, primary_key=True)
	name = db.Column(db.String(32))			# 菜单名字
	level = db.Column(db.Integer)			# 菜单等级
	parent = db.Column(db.Integer)			# 父级菜单
	url = db.Column(db.String(64))			# 链接
	img = db.Column(db.String(128))			# 图片
	permission_id = db.Column(db.Integer)	# 权限

