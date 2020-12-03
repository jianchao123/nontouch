
# coding:utf-8
from db import db


class AdminUser(db.Model):
    __tablename__ = 'admin_user'

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))
    is_active = db.Column(db.Integer)
    company_id = db.Column(db.Integer)
    nickname = db.Column(db.Integer)
    mobile = db.Column(db.Integer)
