# coding:utf-8
from db import db


class CompanyPermission(db.Model):
    """公司权限"""
    __tablename__ = 'company_permission'

    id = db.Column(db.BigInteger, primary_key=True)
    permission_id = db.Column(db.Integer)
    company_id = db.Column(db.Integer)