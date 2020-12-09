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
    def station_list(company_id, bus_route_id, round_trip):
        db.session.commit()
        query = db.session.query(
            BusStation, RouteStationRelation.code,
            RouteStationRelation.round_trip).join(
            RouteStationRelation,
            RouteStationRelation.bus_station_id == BusStation.id).filter(
            BusStation.company_id == company_id)
        if bus_route_id:
            query = query.filter(RouteStationRelation.bus_route_id == bus_route_id)
        if round_trip:
            query = query.filter(RouteStationRelation.round_trip == round_trip)
        count = query.count()
        sets = query.all()
        results = []
        for row in sets:
            station = row[0]
            code = row[1]
            round_trip = row[2]
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
            d['round_trip'] = round_trip
            d['round_trip_name'] = u"去程" if round_trip == 1 else u"返程"
            d['code'] = code
            if bus_route_id:
                bus_route = db.session.query(BusRoute).join(
                    RouteStationRelation,
                    RouteStationRelation.bus_route_id == BusRoute.id).filter(
                    RouteStationRelation.bus_station_id == station.id,
                    RouteStationRelation.bus_route_id == bus_route_id).first()
                d['line_nos'] = bus_route.line_no
            else:
                d['line_nos'] = ''
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

        for row in data:
            try:
                bus_station = db.session.query(BusStation).filter(
                    BusStation.name == row["name"]).one()
                bus_station.name = row["name"]
                bus_station.longitude = row["longitude"]
                bus_station.latitude = row["latitude"]
            except NoResultFound:
                bus_station = BusStation()
                bus_station.name = row["name"]
                bus_station.longitude = row["longitude"]
                bus_station.latitude = row["latitude"]
                bus_station.company_id = company_id
                bus_station.status = 1  # 启用
            db.session.add(bus_station)
            db.session.flush()
            # 添加关系
            route_station_relation = RouteStationRelation()
            route_station_relation.bus_route_id = bus_route
            route_station_relation.bus_station_id = bus_station.id
            route_station_relation.round_trip = round_trip
            route_station_relation.code = row['code']
            route_station_relation.company_id = company_id
            db.session.add(route_station_relation)
        try:
            db.session.commit()
            return 1
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
