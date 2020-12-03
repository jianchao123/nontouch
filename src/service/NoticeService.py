# coding:utf-8
from datetime import datetime
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from database.Notice import Notice


class NoticeService(object):
    """公告"""

    @staticmethod
    def notice_list(company_id, offset, limit):
        """公告列表"""
        db.session.commit()
        query = db.session.query(Notice).filter(Notice.company_id == company_id)
        count = query.count()
        sets = query.offset(offset).limit(limit)

        results = []
        for row in sets:
            d = defaultdict()
            d['id'] = row.id
            d['name'] = row.name
            d['content'] = row.content
            d['create_time'] = row.create_time.strftime('%Y-%m-%d %H:%M:%S')
            d['start_time'] = row.start_time.strftime('%Y-%m-%d %H:%M:%S')
            d['end_time'] = row.end_time.strftime('%Y-%m-%d %H:%M:%S')
            d['priority'] = row.priority
            d['is_active'] = row.is_active
            results.append(d)
        return {'count': count, 'results': results}

    @staticmethod
    def notice_add(company_id, name, content, start_time):
        """添加公告"""
        db.session.commit()
        notice = Notice()
        notice.name = name
        notice.content = content
        notice.start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        notice.end_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        notice.priority = 1
        notice.is_active = 1
        notice.company_id = company_id
        try:
            db.session.add(notice)
            db.session.commit()
            return notice.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def notice_change(pk, name, content, start_time):
        """修改公告"""
        db.session.commit()
        notice = db.session.query(Notice).filter(Notice.id == pk).first()

        notice.name = name
        notice.content = content
        notice.start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

        try:
            db.session.add(notice)
            db.session.commit()
            return notice.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def notice_delete(pk):
        """删除公告"""
        db.session.commit()

        try:
            db.session.query(Notice).filter(
                Notice.id == pk).delete()
            db.session.commit()
            return 1
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def notice_offline_online(pk, is_active):
        """下线上线"""
        db.session.commit()
        notice = db.session.query(Notice).filter(
            Notice.id == pk).first()

        try:
            notice.is_active = is_active
            db.session.commit()
            return notice.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
