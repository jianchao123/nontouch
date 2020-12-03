# coding:utf-8
from datetime import datetime
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from database.Bill import Bill
from database.UserProfile import UserProfile


class BillService(object):

    @staticmethod
    def bill_list(company_id, status, mobile, offset, limit):
        db.session.commit()
        query = db.session.query(Bill, UserProfile).join(
            UserProfile, UserProfile.id == Bill.user_id).filter(
            Bill.company_id == company_id)
        if status:
            query = query.filter(Bill.status == status)
        if mobile:
            query = query.filter(UserProfile.mobile == mobile)
        count = query.count()
        sets = query.offset(offset).limit(limit).all()
        results = []
        for row in sets:
            bill = row[0]
            user = row[1]

            d = defaultdict()
            d['id'] = bill.id
            d['headline'] = bill.headline
            d['headline_type'] = bill.headline_type
            d['bank_name'] = bill.bank_name
            d['bank_account'] = bill.bank_account
            d['email'] = bill.email
            d['bill_no'] = bill.bill_no
            d['pub_date'] = bill.pub_date
            d['enterprise_name'] = bill.enterprise_name
            d['enterprise_address'] = bill.enterprise_address
            d['enterprise_phone'] = bill.enterprise_phone
            d['status'] = bill.status
            d['user_id'] = bill.user_id
            d['user_phone'] = user.mobile
            results.append(d)
        return {'count': count, 'results': results}

    @staticmethod
    def bill_invoicing(pk):
        """
        开发票
        """
        db.session.commit()
        bill = db.session.query(Bill).filter(Bill.id == pk).first()
        if bill.status != 1:
            return -10
        try:
            bill.status = 2
            db.session.commit()
            return {'id': pk}
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
