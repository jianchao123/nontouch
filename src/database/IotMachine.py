# coding:utf-8
from db import db


class IotMachine(db.Model):
    __tablename__ = 'iot_machine'

    id = db.Column(db.BigInteger, primary_key=True)
    mac = db.Column(db.String(128))
    product_id = db.Column(db.Integer)
    product_key = db.Column(db.String(128))
    device_iid = db.Column(db.String(16))
    company_id = db.Column(db.Integer)
