# coding:utf-8
import json
from collections import defaultdict
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

from database.db import db
from database.Company import Company
from database.AdminUser import AdminUser
from database.UserRole import UserRole
from database.Roles import Roles
from database.UserPermissions import UserPermissions

from utils.tools import md5_encrypt


class CompanyService(object):

    @staticmethod
    def company_list(company_id, name, offset, limit):
        db.session.commit()
        query = db.session.query(Company).filter(
            or_(Company.company_id == company_id,
                Company.parent_id == company_id))

        if name:
            query = query.filter(Company.name == name)
        count = query.count()
        sets = query.offset(offset).limit(limit).all()
        results = []
        for row in sets:
            d = defaultdict()
            d['id'] = row.id
            d['province'] = row.province_id
            d['city'] = row.city_id
            d['area'] = row.area_id
            d['create_time'] = row.create_time.strftime('%Y-%m-%d')
            d['house_number'] = row.house_number
            d['line_nos'] = row.line_nos
            d['logo'] = row.logo

            user = db.session.query(AdminUser).filter(
                AdminUser.id == row.admin_user_id).first()
            d['username'] = user.username
            d['mobile'] = user.mobile
            d['name'] = row.name
            d['status'] = row.status
            d['permissions'] = row.permissions
            d['level'] = row.level
            d['parent_id'] = row.parent_id
            results.append(d)
        return {'count': count, 'results': results}

    @staticmethod
    def check_commit_permission(user_company_permissions, commit_permissions):
        """
        检查提交的权限集合
        """
        user_company_permission_ids = \
            [int(row['permission_id'])
             for row in json.loads(user_company_permissions)]
        user_company_permission_ids.sort()
        commit_permission_ids = \
            [int(row['permission_id'])
             for row in json.loads(commit_permissions)]
        commit_permission_ids.sort()
        return set(commit_permission_ids) - set(user_company_permission_ids)

    @staticmethod
    def company_add(company_id, area_id, city_id, province_id, house_number,
                    line_nos, mobile, name, password, permissions,
                    username):
        db.session.commit()
        # 检查上传的权限,添加公司的权限不能超过自己公司的权限
        login_user_company = db.session.query(Company).filter(
            Company.id == company_id).first()
        permissions_tmp = json.loads(permissions)
        if CompanyService.check_commit_permission(
                login_user_company.permissions, permissions):
            return -10
        permission_ids = [row["permission_id"] for row in permissions_tmp]

        # 创建初始化帐号
        new_user = AdminUser()
        new_user.mobile = mobile
        new_user.username = username
        new_user.password = md5_encrypt(password)
        new_user.is_active = 1
        new_user.nickname = username
        db.session.add(new_user)
        db.session.flush()
        new_user_id = new_user.id

        # 创建公司
        company = Company()
        company.area_id = area_id
        company.city_id = city_id
        company.province_id = province_id
        company.house_number = house_number
        company.line_nos = line_nos
        company.name = name
        company.status = 1
        company.permissions = permissions
        company.admin_user_id = new_user_id
        company.level = login_user_company.level + 1
        company.parent_id = company_id
        db.session.add(company)
        db.session.flush()
        new_company_id = company.id
        # 关联id
        company.company_id = new_company_id
        new_user.company_id = new_company_id

        # 创建该公司默认的角色
        role1 = Roles()
        role1.show_name = u'管理员'
        role1.role_name = 'ADMIN'
        role1.company_id = new_company_id
        role1.describe = u'内置角色,不要删除'
        role1.status = 1
        db.session.add(role1)
        db.session.flush()
        new_admin_role_id = role1.id

        role2 = Roles()
        role2.show_name = u'普通'
        role2.role_name = 'GENERAL'
        role2.company_id = new_company_id
        role2.describe = u'内置角色,不要删除'
        role2.status = 1
        db.session.add(role2)

        # 为该公司初始化帐号添加角色
        user_role = UserRole()
        user_role.user_id = new_user_id
        user_role.role_id = new_admin_role_id
        db.session.add(user_role)

        # 为该公司初始化帐号添加权限
        query_set = []

        for permission_id in permission_ids:
            user_permission = UserPermissions()
            user_permission.user_id = new_user_id
            user_permission.permission_id = permission_id
            query_set.append(user_permission)
        db.session.bulk_save_objects(query_set)

        try:
            db.session.commit()
            from msgqueue import producer
            from database.DistrictCode import DistrictCode
            districtcode = db.session.query(DistrictCode).filter(
                DistrictCode.id == area_id).first()
            producer.generate_get_station_msg(
                line_nos, districtcode.ad, new_company_id)
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()
        return new_company_id

    @staticmethod
    def _get_permission_str(cur_permissions, new_permissions):
        result_permissions = []
        new_permission_ids = [row["permission_id"] for row in new_permissions]
        old_permission_ids = [row["permission_id"] for row in cur_permissions]
        delete_permission_ids = list(
            set(old_permission_ids) - set(new_permission_ids))
        # 删除权限
        func = lambda obj: False if obj["permission_id"
                                        ] in delete_permission_ids else True
        result_permissions += list(filter(func, cur_permissions))

        # 增加权限
        add_permission_ids = list(
            set(new_permission_ids) - set(old_permission_ids))
        func = lambda obj: True if obj["permission_id"
                                       ] in add_permission_ids else False
        result_permissions += list(filter(func, new_permissions))
        return json.dumps(result_permissions), \
               delete_permission_ids, add_permission_ids

    @staticmethod
    def company_update(company_id, pk, area_id, city_id, province_id,
                       house_number, mobile, name, new_permissions,
                       username, password, line_nos):
        db.session.commit()
        login_user_company = db.session.query(Company).filter(
            Company.id == company_id).first()
        if CompanyService.check_commit_permission(
                login_user_company.permissions, new_permissions):
            return -10

        new_permissions = json.loads(new_permissions)
        company = db.session.query(Company).filter(Company.id == pk).first()
        if not company:
            return -1

        if name:
            company.name = name
        if area_id:
            company.area_id = area_id
        if city_id:
            company.city_id = city_id
        if province_id:
            company.province_id = province_id
        if house_number:
            company.house_number = house_number
        user = db.session.query(AdminUser).filter(
            AdminUser.username == username)
        if mobile:
            user.mobile = mobile
        if password:
            user.password = md5_encrypt(password)
        if line_nos and line_nos != company.line_nos:
            company.line_nos = line_nos
            from msgqueue import producer
            from database.DistrictCode import DistrictCode
            districtcode = db.session.query(DistrictCode).filter(
                DistrictCode.id == company.area_id).first()
            print "==========================="
            producer.generate_get_station_msg(
                line_nos, districtcode.ad, company.id)

        # 计算已有权限与当前修改权限的差集
        cur_permissions = json.loads(company.permissions)
        permission_str, delete_permission_ids, add_permission_ids = \
            CompanyService._get_permission_str(cur_permissions, new_permissions)

        # 减少该公司下面所有人的权限
        admin_user_sets = db.session.query(AdminUser).filter(
            AdminUser.company_id == company.id).all()
        admin_user_ids = [row.id for row in admin_user_sets]

        db.session.query(UserPermissions).filter(
            UserPermissions.permission_id.in_(delete_permission_ids),
            UserPermissions.user_id.in_(admin_user_ids)).delete(
            synchronize_session=False)

        # 为该公司下面的管理员增加权限
        for user_id in admin_user_ids:
            for permission_id in add_permission_ids:
                user_permission = UserPermissions()
                user_permission.user_id = user_id
                user_permission.permission_id = permission_id
                db.session.add(user_permission)
        company.permissions = permission_str
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def company_disable(pk):
        db.session.commit()
        company = db.session.query(Company).filter(Company.id == pk).first()
        if not company:
            return -1
        if company.status != 1:
            return -3
        company.status = 2   # 禁用
        db.session.add(company)
        # 禁用该公司所有人的帐号
        admin_users = db.session.query(AdminUser).filter(
            AdminUser.company_id == company.id).all()

        for user in admin_users:
            user.is_active = 0  # 禁用

        try:
            db.session.commit()
            return company.id
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def company_enable(pk):
        db.session.commit()
        company = db.session.query(Company).filter(Company.id == pk).first()
        if not company:
            return -1
        if company.status != 2:
            return -3
        company.status = 1  # 启用
        db.session.add(company)
        # 启用该公司所有人的帐号
        admin_users = db.session.query(AdminUser).filter(
            AdminUser.company_id == company.id).all()
        for user in admin_users:
            user.is_active = 1      # 全部激活
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return -2
        finally:
            db.session.close()