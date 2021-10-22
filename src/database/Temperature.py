# coding:utf-8
from db import db
from datetime import datetime


class Temperature(db.Model):
    """温度"""
    __tablename__ = 'temperature'
    id = db.Column(db.BigInteger, primary_key=True)
    temperature = db.Column(db.Integer)
    mobile = db.Column(db.String(16))
    create_time = db.Column(db.DateTime, default=datetime.now)