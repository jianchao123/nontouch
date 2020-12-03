# coding:utf-8
from sqlalchemy.exc import SQLAlchemyError
from database.db import db
from database.Menus import Menus
from database.Permissions import Permissions


class MenuService(object):

    @staticmethod
    def menu_list():
        results = []
        query = db.session.query(Menus, Permissions.permission_name).join(
            Permissions, Permissions.id == Menus.permission_id)
        count = query.count()
        sets = query.all()
        for menu, permission_name in sets:
            results.append({
                'id': menu.id,
                'name': menu.name,
                'level': menu.level,
                'parent': menu.parent,
                'permission_id': menu.permission_id,
                'url': menu.url,
                'img': menu.img,
                'permission_name': permission_name
            })

        return {'count': count, 'results': results}

    @staticmethod
    def menu_update(pk, name, level, parent, permission_id, url, img):
        menu = db.session.query(Menus).filter(Menus.id == pk).first()
        if not menu:
            return -1

        try:
            if name:
                menu.name = name
            if level:
                menu.level = level
            if parent:
                menu.parent = parent
            if permission_id:
                menu.permission_id = permission_id
            if url:
                menu.url = url
            if img:
                menu.img = img
            db.session.add(menu)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
        return 1