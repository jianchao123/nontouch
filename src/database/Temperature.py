# coding:utf-8
from db import db
from datetime import datetime


class Temperature(db.Model):
    """温度"""
    __tablename__ = 'temperature'
    id = db.Column(db.BigInteger, primary_key=True)
    mobile = db.Column(db.String(16))
    temperature = db.Column(db.Float)
    up_timestamp = db.Column(db.String(16))
    device_id = db.Column(db.Integer)
    car_no = db.Column(db.String(32))
    gps = db.Column(db.String(32))
    company_id = db.Column(db.Integer)

