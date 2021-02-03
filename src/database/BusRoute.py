# coding:utf-8
from db import db

status_tuple = (
	(1, u"启用"),
	(2, u"禁用"),	# 线路禁用之后,无法将车辆绑定到线路上
)


class BusRoute(db.Model):
	"""公交线路"""
	__tablename__ = 'bus_route'

	id = db.Column(db.BigInteger, primary_key=True)
	line_no = db.Column(db.String(32))			# 线路名字  131路(地铁天府三街站--金履二路西站)
	fees = db.Column(db.Numeric(11, 6))			# 费用
	amount = db.Column(db.Integer)				# 次数卡每次刷卡所消费的次数
	start_time = db.Column(db.String(32))		# 首发时间
	end_time = db.Column(db.String(32))			# 末班时间
	status = db.Column(db.Integer)				# 状态
	round_trip = db.Column(db.Integer)  		# 往返
	company_id = db.Column(db.Integer)			# 所属公司

