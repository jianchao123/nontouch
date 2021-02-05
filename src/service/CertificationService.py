# coding:utf-8
from decimal import Decimal
import datetime as datetime_m
from dateutil.relativedelta import relativedelta
from datetime import datetime
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from database.PassengerIdentity import PassengerIdentity
from database.Certification import Certification
from database.Company import Company
from database.UserProfile import UserProfile
from database.AdminUser import AdminUser
from database.Identity import Identity


class CertificationService(object):
    """审核记录"""

    @staticmethod
    def certification_list(company_id, mobile, status, identity_id, offset, limit):
        """审核记录"""
        db.session.commit()
        query = db.session.query(
            Certification, Company, UserProfile, Identity, AdminUser).join(
            Company, Company.id == Certification.company_id).join(
            UserProfile, UserProfile.id == Certification.user_id).join(
            Identity, Identity.id == Certification.identity_id).outerjoin(
            AdminUser, AdminUser.id == Certification.verifier_id).filter(
            Certification.company_id == company_id)
        if status:
            query = query.filter(Certification.status == status)
        if identity_id:
            query = query.filter(Identity.id == identity_id)
        if mobile:
            query = query.filter(UserProfile.mobile == mobile)
        count = query.count()
        print count
        sets = query.offset(offset).limit(limit).all()
        results = []
        for row in sets:
            cert = row[0]
            company = row[1]
            user = row[2]
            identity = row[3]
            print row[4]

            d = defaultdict()
            d['id'] = cert.id
            d['company_name'] = company.name
            d['company_id'] = company.id
            d['user_mobile'] = user.mobile
            d['user_signup_time'] = user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
            d['user_id'] = user.id
            d['user_balance'] = str(user.balance)
            d['upload_imgs'] = cert.upload_imgs
            d['status'] = cert.status
            d['pass_reason'] = cert.pass_reason
            d['identity_name'] = identity.name
            d['identity_id'] = identity.id
            d['discount_rate'] = str(identity.discount_rate)
            if cert.status == 2:
                pi = db.session.query(PassengerIdentity).filter(
                    PassengerIdentity.certification_id == cert.id).first()
                admin = db.session.query(AdminUser).filter(
                    AdminUser.id == cert.verifier_id).first()
                d['end_time'] = pi.end_time
                d['date_of_approval'] = cert.date_of_approval.strftime(
                    '%Y-%m-%d %H:%M:%S')
                d['verifier_name'] = admin.username

            results.append(d)
        return {'count': count, 'results': results}

    @staticmethod
    def audit(pk, admin_user_id, status, pass_reason, end_time, discount_rate):
        db.session.commit()
        print pk, admin_user_id
        instance = Certification.query.filter(Certification.id == pk).first()
        if instance.status != 1:
            return -10

        identity = db.session.query(Identity).filter(
            Identity.id == instance.identity_id).first()
        try:
            # 通过
            if status == 2:

                company_id = instance.company_id
                user_id = instance.user_id
                end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

                months = identity.months
                start_time = datetime.now()
                datetime_three_month_ago = start_time + relativedelta(months=months)
                d = datetime_three_month_ago - datetime_m.timedelta(
                    days=datetime_three_month_ago.day)
                section_end_time = d.strftime("%Y-%m-%d %H:%M:%S").split(" ")[
                                       0] + " 23:59:59"
                section_end_time = datetime.strptime(section_end_time,
                                                     "%Y-%m-%d %H:%M:%S")
                section_end_time = end_time if section_end_time >= end_time \
                    else section_end_time

                # 添加乘客身份
                pi = PassengerIdentity()
                pi.identity_name = identity.name
                pi.company_id = company_id
                pi.user_id = user_id
                pi.identity_id = identity.id
                pi.certification_id = instance.id
                pi.status = 1
                pi.discount_rate = Decimal(str(discount_rate))
                pi.end_time = end_time
                pi.section_begin_time = start_time
                pi.section_end_time = section_end_time
                pi.residue_number = identity.number
                db.session.add(pi)

            instance.status = status
            instance.pass_reason = pass_reason
            instance.date_of_approval = datetime.now()
            instance.verifier_id = admin_user_id
            db.session.commit()
            return {'id': instance.id}
        except SQLAlchemyError:
            import traceback
            print traceback.format_exc()
            db.session.rollback()
            return -2
        finally:
            db.session.close()


