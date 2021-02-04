# coding:utf-8
from db import db
from datetime import datetime

headline_tuple = (
	(1, "企业单位"),
	(2, "个人/非企业单位")
)
status_tuple = (
	(1, "待开票"),
	(2, "已开票")
)


class Bill(db.Model):
	"""票据"""
	__tablename__ = 'bill'

	id = db.Column(db.BigInteger, primary_key=True)
	headline = db.Column(db.String(32))			# 抬头
	headline_type = db.Column(db.Integer)		# 抬头类型
	bank_name = db.Column(db.String(32))		# 开户行名字
	bank_account = db.Column(db.String(32))		# 银行账户
	email = db.Column(db.String(32))			# 邮箱
	bill_no = db.Column(db.String(32))			# 发票编号
	pub_date = db.Column(db.DateTime, default=datetime.now)	# 开票日期
	enterprise_name = db.Column(db.String(32))			# 企业名称
	enterprise_address = db.Column(db.String(32))		# 企业地址
	enterprise_phone = db.Column(db.String(32))			# 企业号码
	amounts = db.Column(db.Numeric(11, 6))				# 总金额
	status = db.Column(db.Integer)						# 状态
	user_id = db.Column(db.Integer)						# 开票用户
	company_id = db.Column(db.Integer)					# owner_id

