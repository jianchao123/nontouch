# coding:utf-8
from db import db


class DistrictCode(db.Model):
	"""区域代码"""
	__tablename__ = 'district_code'

	id = db.Column(db.BigInteger, primary_key=True)
	name = db.Column(db.String(30))			# 城市地区中文名称
	ad = db.Column(db.String(6))			# 高德地图区域编码adcode
	city = db.Column(db.String(6)) 			# 城市编码
	pinyin = db.Column(db.String(100))		# 城市地区中文拼音
	level = db.Column(db.Integer)			# 地区层级(1,2,3)
