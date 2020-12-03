# coding:utf-8
from db import db


class Button(db.Model):
    """按钮"""
    __tablename__ = 'button'

    id = db.Column(db.BigInteger, primary_key=True)
    btn_element_id = db.Column(db.Integer)
    permission_id = db.Column(db.Integer)
    btn_name = db.Column(db.String(32))
    parent_menu_id = db.Column(db.Integer)

