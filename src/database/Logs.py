# coding:utf-8
from db import db
from datetime import datetime


class Logs(db.Model):
	__tablename__ = 'logs'

	id = db.Column(db.BigInteger, primary_key=True)
	user_pk = db.Column(db.Integer)
	username = db.Column(db.String(32))
	action_name = db.Column(db.Integer)
	obj = db.Column(db.Text())
	create_time = db.Column(db.DateTime, default=datetime.now)
	ip = db.Column(db.String(32))
	company_id = db.Column(db.Integer)
	user_id = db.Column(db.Integer)
