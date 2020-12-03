# coding:utf-8
from db import db
from datetime import datetime
GENDER_CHOICES = (
	(0, 'Secrecy'),
	(1, 'Male'),
	(2, 'Female'),
)


class UserProfile(db.Model):
	__tablename__ = 'user_profile'

	id = db.Column(db.BigInteger, primary_key=True)
	password = db.Column(db.String(128))
	last_login = db.Column(db.DateTime, default=datetime.now)
	username = db.Column(db.String(150))
	email = db.Column(db.String(254))
	is_active = db.Column(db.Integer)
	date_joined = db.Column(db.DateTime, default=datetime.now)
	mobile = db.Column(db.String(11))
	nickname = db.Column(db.String(20))
	id_card = db.Column(db.String(18))
	balance = db.Column(db.Numeric(11, 6))
	avatar = db.Column(db.String(128))
	gender = db.Column(db.Integer)
	birthday = db.Column(db.Date)
	wx_open_id = db.Column(db.String(32))
	is_open_face_rgz = db.Column(db.Integer)	# 是否开通人脸识别
	invite_code = db.Column(db.String(11))		# 邀请码
	company_id = db.Column(db.Integer)			# 公司id