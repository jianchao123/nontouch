# coding:utf-8
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from database.Temperature import Temperature


class TemperatureService(object):

    @staticmethod
    def temperature_list(company_id, offset, limit):
        db.session.commit()
        query = db.session.query(Temperature).filter(
            Temperature.company_id == company_id).order_by(
            Temperature.id.desc())
        count = query.count()
        results = query.offset(offset).limit(limit).all()
        data = []
        for row in results:
            data.append({
                "id": row.id,
                "mobile": row.mobile,
                "temperature": row.temperature,
                "up_timestamp": row.up_timestamp,
                "device_id": row.device_id,
                "car_no": row.car_no,
                "gps": row.gps
            })
        return {'count': count, 'results': data}

