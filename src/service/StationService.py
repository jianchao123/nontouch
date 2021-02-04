# coding:utf-8
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from database.db import db
from database.BusStation import BusStation
from database.BusRoute import BusRoute
from database.RouteStationRelation import RouteStationRelation
from database.Company import Company


class StationService(object):

    @staticmethod
    def station_list(company_id, bus_route_id):
        db.session.commit()
        query = db.session.query(
            BusStation, RouteStationRelation.code).join(
            RouteStationRelation,
            RouteStationRelation.bus_station_id == BusStation.id).filter(
            BusStation.company_id == company_id)
        if bus_route_id:
            query = query.filter(
                RouteStationRelation.bus_route_id == bus_route_id)
        count = query.count()
        sets = query.all()
        results = []
        for row in sets:
            station = row[0]
            code = row[1]
            d = defaultdict()
            d['id'] = station.id
            d['name'] = station.name
            d['status'] = station.status
            d['status_name'] = u'启用' if station.status == 1 else u'禁用'
            d['longitude'] = str(station.longitude)
            d['latitude'] = str(station.latitude)
            d['company_id'] = station.company_id
            company = db.session.query(Company).filter(
                Company.id == station.company_id).first()
            d['company_name'] = company.name

            d['code'] = code
            d['number'] = station.number
            if bus_route_id:
                bus_route = db.session.query(BusRoute).filter(
                    BusRoute.id == bus_route_id).first()
                d['line_no'] = bus_route.line_no
            else:
                d['line_no'] = ''
            results.append(d)
        return {'count': count, 'results': results}

    @staticmethod
    def station_add(company_id, data, bus_route, round_trip):
        """
        先删除所有关系记录,然后添加
        """
        db.session.commit()
        db.session.query(RouteStationRelation).filter(
            RouteStationRelation.bus_route_id == bus_route,
            RouteStationRelation.round_trip == round_trip).delete()

        inx = 1
        for station_id in data.split(','):
            bus_station = db.session.query(BusStation).filter(
                BusStation.id == station_id).first()

            # 添加关系
            route_station_relation = RouteStationRelation()
            route_station_relation.bus_route_id = bus_route.id
            route_station_relation.bus_station_id = bus_station.id
            route_station_relation.round_trip = bus_route.round_trip
            route_station_relation.code = inx
            route_station_relation.company_id = company_id
            db.session.add(route_station_relation)
            inx += 1
        try:
            db.session.commit()
            return 1
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
