# coding:utf-8
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from database.Roles import Roles


class RoleService(object):

    @staticmethod
    def role_list(company_id, offset, limit):

        results = []
        query = db.session.query(Roles).filter(
            Roles.company_id == company_id)

        count = query.count()
        sets = query.offset(offset).limit(limit).all()
        for role in sets:
            results.append({
                'id': role.id,
                'company': role.company_id,
                'create_time': role.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'describe': role.describe,
                'show_name': role.show_name,
                'status': role.status
            })

        return {'count': count, 'results': results}

    @staticmethod
    def role_update(pk, show_name, describe):
        role = db.session.query(Roles).filter(Roles.id == pk).first()
        if not role:
            return -1
        try:
            if show_name:
                role.show_name = show_name
            if describe:
                role.describe = describe
            db.session.add(role)
            db.session.commit()
            return role.id

        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def role_add(company_id, role_name, show_name, describe):

        roles = db.session.query(Roles).filter(
            Roles.role_name == role_name).first()
        if roles:
            return -10
        try:
            role = Roles()
            role.role_name = role_name
            role.describe = describe
            role.company_id = company_id
            role.show_name = show_name
            role.status = 1     # 1有效
            db.session.add(role)
            db.session.flush()
            new_id = role.id
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
        return new_id

    @staticmethod
    def role_delete(pk):
        role = db.session.query(Roles).filter(Roles.id == pk).first()
        if not role:
            return -1
        try:
            role.status = 10        # 10删除
            db.session.add(role)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
        return pk