# coding:utf-8
from db import db
from datetime import datetime


class FaceImg(db.Model):
	"""人脸图片"""
	__tablename__ = 'face_img'

	id = db.Column(db.BigInteger, primary_key=True)	# fid
	img = db.Column(db.Text())						# 图片流(BASE64编码)
	baidu_user_id = db.Column(db.String(32))		# 手机号
	group_id = db.Column(db.String(32))				# 在百度上的分组
	oss_url = db.Column(db.String(128))				# 在OSS的url
	parent_mobile = db.Column(db.String(32))		# 父级mobile
	is_sub_account = db.Column(db.Integer)			# 是否子帐号
	sub_account_name = db.Column(db.String(32))		# 子帐号名称
	face_id = db.Column(db.String(32))				# 百度facetoken
	face_last_time = db.Column(db.DateTime, default=datetime.now)	# 人脸最后更新时间
	delete_time = db.Column(db.DateTime, default=datetime.now)		# 删除时间
	status = db.Column(db.Integer)		# 1未添加人脸 2待生成feature 3有效 4生成失败 10删除
	user_id = db.Column(db.Integer)		# 乘客
	company_id = db.Column(db.Integer)
	feature = db.Column(db.String(1024))
	feature_crc = db.Column(db.String(32))

