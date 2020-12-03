# coding:utf-8
from db import db
from datetime import datetime


class BcEveryDayData(db.Model):
	"""公交公司每日数据"""
	__tablename__ = 'bc_every_day_data'

	id = db.Column(db.BigInteger, primary_key=True)
	income = db.Column(db.Numeric(11, 6))		# 收入
	passenger_flow = db.Column(db.Integer)		# 客流
	kilometre = db.Column(db.Integer)			# 里程
	number_passengers = db.Column(db.Integer)	# 乘车人数
	dcccrs = db.Column(db.Integer)				# 多次乘车人数
	face_count = db.Column(db.Integer)			# 人脸支付数量
	ic_card_count = db.Column(db.Integer)		# IC卡支付数量
	qrcode_count = db.Column(db.Integer)		# 二维码支付数量
	cash_count = db.Column(db.Integer)			# 现金支付数量
	face_rate = db.Column(db.Numeric(11, 6))	# 刷脸支付占比
	ic_card_rate = db.Column(db.Numeric(11, 6))	# ic卡支付占比
	qrcode_rate = db.Column(db.Numeric(11, 6))	# 二维码支付占比
	cash_rate = db.Column(db.Numeric(11, 6))	# 现金支付占比
	data_date = db.Column(db.Date)				# 数据日期
	settlement_time = db.Column(db.DateTime, default=datetime.now) # 结算时间
	company_id = db.Column(db.Integer)	# 所属公司
