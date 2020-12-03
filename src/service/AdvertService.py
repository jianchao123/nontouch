# coding:utf-8
from datetime import datetime
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from database.Advert import Advert


class AdvertService(object):
    """公告"""

    @staticmethod
    def advert_list(company_id, offset, limit):
        """公告列表"""
        db.session.commit()
        query = db.session.query(Advert).filter(Advert.company_id == company_id)
        count = query.count()
        sets = query.offset(offset).limit(limit)

        results = []
        for row in sets:
            d = defaultdict()
            d['id'] = row.id
            d['name'] = row.name
            d['image'] = row.image
            d['url'] = row.url
            d['create_time'] = row.create_time.strftime('%Y-%m-%d %H:%M:%S')
            d['start_time'] = row.start_time.strftime('%Y-%m-%d %H:%M:%S')
            d['end_time'] = row.end_time.strftime('%Y-%m-%d %H:%M:%S')
            d['is_active'] = row.is_active
            d['adv_location'] = row.adv_location
            results.append(d)
        return {'count': count, 'results': results}

    @staticmethod
    def advert_add(company_id, name, image, url, start_time,
                   end_time, is_active, adv_location):
        """添加公告"""

        db.session.commit()
        advert = Advert()
        advert.name = name
        advert.image = image
        advert.url = url
        advert.start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        advert.end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        advert.is_active = is_active
        advert.adv_location = adv_location
        advert.company_id = company_id
        try:
            db.session.add(advert)
            db.session.commit()
            return advert.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def advert_change(pk, name, image, url, start_time,
                      end_time, is_active, adv_location):
        """修改公告"""
        db.session.commit()
        advert = db.session.query(Advert).filter(Advert.id == pk).first()

        advert.name = name
        advert.image = image
        advert.url = url
        advert.start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        advert.end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        advert.is_active = is_active
        advert.adv_location = adv_location
        try:
            db.session.commit()
            return advert.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def advert_delete(pk):
        """删除公告"""
        db.session.commit()

        try:
            db.session.query(Advert).filter(
                Advert.id == pk).delete()
            db.session.commit()
            return 1
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def advert_offline_online(pk, is_active):
        """下线上线"""
        db.session.commit()
        advert = db.session.query(Advert).filter(
            Advert.id == pk).first()

        try:
            advert.is_active = is_active
            db.session.commit()
            return advert.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
