# coding:utf-8
from collections import defaultdict
from database.db import db
from database.DistrictCode import DistrictCode


class DistrictCodeService(object):

    @staticmethod
    def district_code_list():
        result = []
        queryset = db.session.query(DistrictCode).all()
        for q in queryset:
            if q.level == 1:
                province = defaultdict()
                province['name'] = q.name
                province['id'] = q.ad
                province["pk"] = q.id
                province['city'] = []
                result.append(province)
            elif q.level == 2:
                city = defaultdict()
                city['name'] = q.name
                city['id'] = q.ad
                city["pk"] = q.id
                city['county'] = []
                province['city'].append(city)
            else:
                county = defaultdict()
                county['name'] = q.name
                county['id'] = q.ad
                county["pk"] = q.id
                if city.get('county') is not None:
                    city['county'].append(county)
        return result
