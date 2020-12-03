# coding:utf-8
from datetime import datetime
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from database.Feedback import Feedback


class FeedbackService(object):
    """反馈"""

    @staticmethod
    def feedback_list(company_id, offset, limit):
        """反馈列表"""
        db.session.commit()
        query = db.session.query(Feedback).filter(
            Feedback.company_id == company_id)
        count = query.count()
        sets = query.offset(offset).limit(limit)

        results = []
        for row in sets:
            d = defaultdict()
            d['id'] = row.id
            d['content'] = row.content
            d['start_time'] = row.start_time.strftime('%Y-%m-%d %H:%M:%S')
            d['end_time'] = row.end_time.strftime('%Y-%m-%d %H:%M:%S')
            d['remarks'] = row.remarks
            d['type_id'] = row.type_id
            d['user_id'] = row.user_id
            results.append(d)
        return {'count': count, 'results': results}

    @staticmethod
    def feedback_change(pk, remarks):
        """修改反馈"""
        db.session.commit()
        feedback = db.session.query(Feedback).filter(
            Feedback.id == pk).first()

        try:
            feedback.remarks = remarks
            db.session.commit()
            return feedback.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
