# coding:utf-8
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from database.Roles import Roles


class TemperatureService(object):

    @staticmethod
    def temperature_list(company_id, offset, limit):
        db.session.commit()

        return {'count': 9, 'results': {}}

