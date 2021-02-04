# coding:utf-8
from datetime import datetime
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from database.LostAndFound import LostAndFound
from database.AdminUser import AdminUser
from database.UserProfile import UserProfile


class LostAndFoundService(object):
    """公告"""

    @staticmethod
    def lostandfound_list(company_id, offset, limit):
        """公告列表"""
        db.session.commit()
        query = db.session.query(LostAndFound).filter(
            LostAndFound.company_id == company_id).filter(
            LostAndFound.status != 10)
        count = query.count()
        sets = query.offset(offset).limit(limit)

        results = []
        for row in sets:
            d = defaultdict()
            if row.is_admin_publish:
                admin_user = db.session.query(AdminUser).filter(
                    AdminUser.id == row.create_user_id).first()
                d['create_user_name'] = u'管理员'
            else:
                user_profile = db.session.query(UserProfile).filter(
                    UserProfile.id == row.create_user_id).first()
                d['create_user_name'] = user_profile.mobile

            d['id'] = row.id
            d['description'] = row.description
            d['city'] = row.city
            d['line_no'] = row.line_no
            d['contacts'] = row.contacts
            d['status'] = row.status
            d['imgs'] = row.imgs
            d['is_admin_publish'] = row.is_admin_publish
            d['create_user_id'] = row.create_user_id

            d['create_time'] = row.create_time.strftime('%Y-%m-%d %H:%M:%S')
            results.append(d)
        return {'count': count, 'results': results}

    @staticmethod
    def lostandfound_add(company_id, user_id, description, city,
                         line_no, contacts, imgs):
        """
        添加公告
        """

        db.session.commit()
        lostandfound = LostAndFound()
        lostandfound.description = description
        lostandfound.city = city
        lostandfound.line_no = line_no
        lostandfound.contacts = contacts
        lostandfound.status = 1  # 未认领
        lostandfound.imgs = imgs
        lostandfound.is_admin_publish = 1
        lostandfound.create_user_id = user_id
        lostandfound.company_id = company_id
        try:
            db.session.add(lostandfound)
            db.session.commit()
            return lostandfound.id
        except SQLAlchemyError:
            import traceback
            print traceback.format_exc()
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def lostandfound_change(pk, description, city,
                            line_no, contacts, imgs):
        """修改公告"""
        db.session.commit()
        lostandfound = db.session.query(LostAndFound).filter(
            LostAndFound.id == pk).first()

        lostandfound.description = description
        lostandfound.city = city
        lostandfound.line_no = line_no
        lostandfound.contacts = contacts
        lostandfound.imgs = imgs
        try:
            db.session.commit()
            return lostandfound.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def lostandfound_delete(pk):
        """删除公告"""
        db.session.commit()
        lostandfound = db.session.query(LostAndFound).filter(
            LostAndFound.id == pk).first()

        try:
            lostandfound.status = 10
            db.session.commit()
            return lostandfound.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
