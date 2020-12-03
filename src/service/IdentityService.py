# coding:utf-8
from decimal import Decimal
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from database.Identity import Identity
from database.Company import Company
from database.PassengerIdentity import PassengerIdentity


class IdentityService(object):
    """身份"""

    @staticmethod
    def identity_list(company_id, offset, limit):
        """身份列表"""
        db.session.commit()
        query = db.session.query(Identity, Company).join(
            Company, Company.id == Identity.company_id).filter(
            Identity.company_id == company_id).filter(Identity.status != 10)
        count = query.count()
        sets = query.offset(offset).limit(limit)

        results = []
        for row in sets:
            identity = row[0]
            company = row[1]

            d = defaultdict()
            d['id'] = identity.id
            d['name'] = identity.name
            d['company_id'] = identity.company_id
            d['company_name'] = company.name
            d['description'] = identity.description
            d['months'] = identity.months
            d['number'] = identity.number
            d['status'] = identity.status
            d['discount_rate'] = str(identity.discount_rate)
            d['create_time'] = identity.create_time.strftime('%Y-%m-%d %H:%M:%S')
            results.append(d)
        return {'count': count, 'results': results}

    @staticmethod
    def identity_delete(pk):
        db.session.commit()
        identity = db.session.query(Identity).filter(Identity.id == pk).first()
        if not identity:
            return -1
        pi_count = db.session.query(PassengerIdentity).filter(
            PassengerIdentity.identity_id == pk).count()
        if pi_count:
            return -10

        try:
            identity.status = 10
            db.session.commit()
            return {'id': pk}
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def identity_add(company_id, description, discount_rate, months, name, number):
        db.session.commit()
        count = db.session.query(Identity).filter(
            Identity.company_id == company_id, Identity.name == name).count()
        if count:
            return -10
        try:
            identity = Identity()
            identity.description = description
            identity.discount_rate = Decimal(str(discount_rate))
            identity.months = int(months)
            identity.name = name
            identity.number = int(number)
            identity.status = 1     # 使用中
            identity.company_id = company_id
            db.session.add(identity)
            db.session.commit()
            return {'id': identity.id}
        except SQLAlchemyError:
            import traceback
            print traceback.format_exc()
            db.session.rollback()
            return -2
        finally:
            db.session.close()

