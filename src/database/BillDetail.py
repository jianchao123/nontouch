# coding:utf-8
from db import db


class BillDetail(db.Model):
	"""票据详情"""
	__tablename__ = 'bill_detail'

	id = db.Column(db.BigInteger, primary_key=True)
	bill_id = db.Column(db.Integer)		# 票据
	recharge_id = db.Column(db.Integer)	# 充值订单id
	company_id = db.Column(db.Integer)
