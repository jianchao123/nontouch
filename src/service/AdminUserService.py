# coding:utf-8
import json
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError

from database.db import db
from database.AdminUser import AdminUser
from database.Permissions import Permissions
from database.UserPermissions import UserPermissions
from database.Menus import Menus
from database.UserRole import UserRole
from database.Company import Company
from database.Roles import Roles

from utils.rest import md5_encrypt
from ext import conf
from ext import cache


class AdminUserService(object):

    TOKEN_ID_KEY = 'hash:token.id:{}'
    INVALID_USER_ID = -1
    USER_OPERATIONS = 'user:operations:{}'

    @staticmethod
    def admin_user_list(company_id, offset, limit, username):
        db.session.commit()
        query = db.session.query(AdminUser, UserRole).join(
            UserRole, UserRole.user_id == AdminUser.id).filter(
            AdminUser.company_id == company_id)
        if username:
            query = query.filter(AdminUser.username == username)

        results = []
        count = query.count()
        sets = query.offset(offset).limit(limit).all()
        company = db.session.query(Company).filter(
            Company.id == company_id).first()
        for row in sets:
            admin_user = row[0]
            user_role = row[1]
            role = db.session.query(Roles).filter(
                Roles.id == user_role.role_id).first()

            d = defaultdict()
            d['pk'] = admin_user.id
            d['is_active'] = admin_user.is_active
            d['mobile'] = admin_user.mobile
            d['nickname'] = admin_user.nickname
            d['show_name'] = role.show_name
            d['username'] = admin_user.username
            d['company_name'] = company.name
            results.append(d)
        return {'count': count, 'results': results}

    @staticmethod
    def check_commit_permission(company_id, commit_permissions):
        """
        检查提交的权限集合
        """
        db.session.commit()
        from CompanyService import CompanyService
        user_company_permission_ids = \
            CompanyService.get_company_permission_id_list(company_id)
        user_company_permission_ids.sort()
        commit_permission_ids = \
            [int(row['permission_id'])
             for row in json.loads(commit_permissions)]
        commit_permission_ids.sort()
        print "check_commit_permission"
        print set(commit_permission_ids) - set(user_company_permission_ids)
        return set(commit_permission_ids) - set(user_company_permission_ids)

    @staticmethod
    def admin_user_update(company_id, pk, is_active, permissions, role,
                          username, password, nickname):
        """修改PC端用户
         permission
        [{"permission_id":1,"permission_name":"增加广告","group":"广告"}]
        """
        db.session.commit()
        login_user_company = db.session.query(Company).filter(
            Company.id == company_id).first()
        if AdminUserService.check_commit_permission(
                login_user_company.id, permissions):
            return -10

        permissions = json.loads(permissions)
        user = db.session.query(AdminUser).filter(
            AdminUser.id == pk).first()
        if not user:
            return -1

        try:
            if is_active in (1, -1):
                user.is_active = 1 if is_active == 1 else 0
            if username:
                user.username = username
            if role:
                user_role = db.session.query(UserRole).filter(
                    UserRole.user_id == pk).first()
                user_role.role_id = role

            if permissions:

                # 删除该用户所有权限
                db.session.query(UserPermissions).filter(
                        UserPermissions.user_id == pk).delete()

                # 重新添加权限
                user_permission_objs = []
                for row in permissions:
                    up = UserPermissions()
                    up.user_id = pk
                    up.permission_id = row['permission_id']
                    user_permission_objs.append(up)
                db.session.bulk_save_objects(user_permission_objs)
            if password:
                user.password = md5_encrypt(password)
            if nickname:
                user.nickname = nickname
            db.session.add(user)
            db.session.commit()
            return user.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def admin_user_disable_enable(pk, is_active):
        """
        禁用或启用
        """
        db.session.commit()
        user = db.session.query(AdminUser).filter(
            AdminUser.id == pk).first()
        if not user:
            return -1

        try:
            user.is_active = is_active
            db.session.add(user)
            db.session.commit()
            return user.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def admin_user_add(company_id, password,
                       username, permissions, role):
        db.session.commit()
        login_user_company = db.session.query(Company).filter(
            Company.id == company_id).first()
        # 检查提交的权限是否大于公司
        if AdminUserService.check_commit_permission(
                login_user_company.id, permissions):
            return -10
        permissions = json.loads(permissions)
        try:

            user = AdminUser()
            user.password = md5_encrypt(password)
            user.username = username
            user.is_active = 1
            user.company_id = company_id
            user.nickname = username
            user.mobile = username

            db.session.add(user)
            db.session.flush()
            new_id = user.id

            # 添加角色
            user_role = UserRole()
            user_role.user_id = new_id
            user_role.role_id = role
            user_role.company_id = company_id
            db.session.add(user_role)

            # 添加权限
            user_permission_objs = []
            for row in permissions:
                up = UserPermissions()
                up.user_id = new_id
                up.permission_id = row['permission_id']
                up.company_id = company_id
                user_permission_objs.append(up)
            db.session.bulk_save_objects(user_permission_objs)

            db.session.commit()
            return new_id
        except SQLAlchemyError:
            db.session.rollbakc()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def admin_user_retrieve(pk):
        db.session.commit()
        user = db.session.query(AdminUser).filter(
            AdminUser.id == pk).first()
        if not user:
            return -1
        d = defaultdict()

        user_role = db.session.query(UserRole).filter(
            UserRole.user_id == pk).first()
        d['company_id'] = user.company_id
        d['role'] = user_role.role_id
        d['is_active'] = user.is_active
        d['mobile'] = user.mobile
        d['nickname'] = user.nickname
        d['username'] = user.username
        # 获取权限
        user_permissions = db.session.query(Permissions).join(
            UserPermissions, UserPermissions.permission_id == Permissions.id
        ).filter(UserPermissions.user_id == pk).all()
        permissions = []
        for row in user_permissions:
            permissions.append({
                'permission_name': row.permission_name,
                'group': row.group,
                'permission_id': row.id
            })
        d['permissions'] = permissions
        return d

    @staticmethod
    def parse_dict(menu, find_parent, target_node):
        if find_parent == menu["id"]:
            target_node.append(menu)
        child_node = menu["childNode"]
        if child_node:
            for x in child_node:
                AdminUserService.parse_dict(x, find_parent, target_node)

    @staticmethod
    def get_menus(menus):
        main_dict = {
            "name": "main",
            "id": 1,
            "img": "",
            "childNode": [],
            "parent": "",
            "level": 0
        }
        for row in menus:
            level = row.level
            d = {
                "name": row.name,
                "id": row.id,
                "img": row.img,
                "childNode": "",
                "parent": row.parent,
                "level": level,
                "url": row.url
            }
            level -= 1
            menu = row
            while level != 0:
                target_node = []
                # menu_list里面是否已经存在同层级同parent的元素
                AdminUserService.parse_dict(main_dict, menu.parent, target_node)
                if target_node:
                    childs = target_node[0]["childNode"]
                    child_ids = [row['id'] for row in childs]
                    if d["id"] not in child_ids:
                        childs.append(d)
                else:
                    menu = db.session.query(Menus).filter(
                        Menus.id == menu.parent).first()
                    d = {
                        "name": menu.name,
                        "id": menu.id,
                        "img": menu.img,
                        "childNode": [d],
                        "parent": menu.parent,
                        "level": level
                    }
                level -= 1
            if d["level"] == 1:
                main_dict["childNode"].append(d)
        return main_dict

    @staticmethod
    def addition_button(user_menus, user_permission_ids):
        db.session.commit()
        from database.Button import Button
        for menu in user_menus:
            menu_id = menu['id']
            buttons = db.session.query(Button).filter(
                Button.parent_menu_id == menu_id,
                Button.permission_id.in_(user_permission_ids)).all()
            menu['button'] = [{'btn_element_id': row.btn_element_id,
                               'btn_name': row.btn_name}
                              for row in buttons]
            AdminUserService.addition_button(menu['childNode'], user_permission_ids)

    @staticmethod
    def login_user_info(user_id):
        db.session.commit()
        # 登录用户的个人信息和公司信息
        user = db.session.query(AdminUser).filter(
            AdminUser.id == user_id).first()
        company = db.session.query(Company).filter(
            Company.id == user.company_id).first()
        from service.CompanyService import CompanyService
        print CompanyService.get_company_permission_id_list(company.id)

        permission_set = db.session.query(Permissions).filter(
            Permissions.id.in_(CompanyService.get_company_permission_id_list(company.id))).all()
        print "=========================="
        print permission_set
        # 该用户所属的公司权限
        company_permissions = []
        for row in permission_set:
            company_permissions.append(
                {'id': row.id,
                 'permission_name': row.permission_name,
                 'group': row.group,
                 'is_show': row.is_show,
                 'is_default': row.is_default})
        # 该用户所属公司的所有角色
        company_roles = []
        company_role_sets = db.session.query(Roles).filter(
            Roles.company_id == company.id).all()
        for row in company_role_sets:
            company_roles.append({
                'id': row.id, 'company': row.company_id,
                'show_name': row.show_name, 'describe': row.describe,
                'status': row.status, 'create_time':
                    row.create_time.strftime('%Y-%m-%d %H:%M:%S')})

        # 用户权限
        sets = db.session.query(UserPermissions).filter(
            UserPermissions.user_id == user.id).all()
        user_permission_ids = [row.permission_id for row in sets]

        # 菜单
        menu_sets = db.session.query(Menus).filter(
            Menus.permission_id.in_(user_permission_ids))
        main_dict = AdminUserService.get_menus(menu_sets)
        AdminUserService.addition_button(
            main_dict['childNode'], user_permission_ids)
        user_menus = main_dict["childNode"]

        return {'company_id': company.id, 'company_logo': company.logo,
                'company_name': company.name,
                'company_permissions': company_permissions,
                'company_roles': company_roles,
                'menus': user_menus,
                'mobile': user.mobile,
                'nickname': user.nickname,
                'username': user.username}

    @staticmethod
    def change_pwd(user_id, old_password, new_password):
        """修改密码"""
        db.session.commit()
        user = db.session.query(AdminUser).filter(
            AdminUser.id == user_id).first()
        if md5_encrypt(old_password) != user.password:
            return -10
        user.password = md5_encrypt(new_password)
        try:
            db.session.commit()
            return {'id': user_id}
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def get_user_by_username(username):
        """根据用户名获取"""
        db.session.commit()
        user = db.session.query(AdminUser).filter(
            AdminUser.username == username).first()
        print user
        if not user:
            return -1
        if not user.is_active:
            return -2
        u = {
            'id': user.id,
            'username': user.username,
            'password': user.password
        }
        return u

    @staticmethod
    def login(user_id, token):
        cache.set(AdminUserService.TOKEN_ID_KEY.format(token), user_id)
        cache.expire(AdminUserService.TOKEN_ID_KEY.format(token), 60 * 60 * 2)