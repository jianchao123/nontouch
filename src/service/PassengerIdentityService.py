# coding:utf-8
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from database.PassengerIdentity import PassengerIdentity
from database.Company import Company
from database.UserProfile import UserProfile
from database.Identity import Identity


class PassengerIdentityService(object):

    @staticmethod
    def passenger_identity_list(company_id, status, identity_id, offset, limit):
        db.session.commit()
        query = db.session.query(PassengerIdentity, Company,
                                 UserProfile, Identity).join(
            Company, Company.id == PassengerIdentity.company_id).join(
            UserProfile, UserProfile.id == PassengerIdentity.user_id).join(
            Identity, Identity.id == PassengerIdentity.identity_id).filter(
            PassengerIdentity.company_id == company_id).filter(
            PassengerIdentity.status != 10)
        if status:
            query = query.filter(PassengerIdentity.status == status)
        if identity_id:
            query = query.filter(PassengerIdentity.identity_id == identity_id)
        count = query.count()
        sets = query.offset(offset).limit(limit).all()
        results = []
        for row in sets:
            pi = row[0]
            company = row[1]
            user = row[2]
            identity = row[3]

            d = defaultdict()
            d['id'] = pi.id
            d['company_name'] = company.name
            d['user_mobile'] = user.mobile
            d['user_id'] = user.id
            d['identity_id'] = identity.id
            d['identity_name'] = identity.name
            d['status'] = identity.status
            d['section_begin_time'] = \
                pi.section_begin_time.strftime('%Y-%m-%d %H:%M:%S')
            d['end_time'] = pi.end_time.strftime('%Y-%m-%d %H:%M:%S')
            d['section_end_time'] = \
                pi.section_end_time.strftime('%Y-%m-%d %H:%M:%S')
            d['residue_number'] = pi.residue_number
            d['discount_rate'] = str(pi.discount_rate)
            d['company_id'] = pi.company_id
            d['certification_id'] = pi.certification_id
            results.append(d)
        return {'count': count, 'results': results}

    @staticmethod
    def passenger_identity_delete(pk):
        """
        """
        db.session.commit()
        pi = db.session.query(PassengerIdentity).filter(
            PassengerIdentity.id == pk).first()
        if pi.status not in (1, 2):
            return -10
        try:
            pi.status = 10
            db.session.commit()
            return {'id': pk}
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
