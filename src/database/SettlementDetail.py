# coding:utf-8
from db import db
from datetime import datetime


class SettlementDetail(db.Model):
    """结算详情"""
    __tablename__ = 'settlement_detail'

    id = db.Column(db.BigInteger, primary_key=True)
    settlement_id = db.Column(db.Integer)
    order_id = db.Column(db.Integer)
    company_id = db.Column(db.Integer)