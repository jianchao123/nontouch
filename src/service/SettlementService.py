# coding:utf-8
import json
from collections import defaultdict
from decimal import Decimal
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from database.db import db
from database.Settlement import Settlement
from database.Company import Company
from database.SettlementDetail import SettlementDetail
from database.Order import Order
from database.UserProfile import UserProfile

from utils import xls


class SettlementService(object):

    @staticmethod
    def settlement_list(company_id, offset, limit):
        """结算列表"""
        query = db.session.query(Settlement)
        # 不是无感行
        if company_id != 1:
            query = query.filter(Settlement.company_id == company_id)
        count = query.count()
        sets = query.offset(offset).limit(limit)
        results = []
        for row in sets:
            company_id = row.company_id
            company = db.session.query(Company).filter(
                Company.id == company_id).first()

            results.append({
                'id': row.id,
                'create_time': row.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'start_time': row.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': row.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': row.status,
                'amount': str(row.amount),
                'company_id': row.company_id,
                'company_name': company.name,
                'xls_oss_url': row.xls_oss_url
            })
        return {'count': count, 'results': results}

    @staticmethod
    def settlement_retrieve(pk):
        """检索结算"""
        db.session.commit()
        settlement = db.session.query(Settlement).filter(
            Settlement.id == pk).first()
        if not settlement:
            return -1

        company = db.session.query(Company).filter(
            Company.id == settlement.company_id).first()

        sets = db.session.query(SettlementDetail, Order).join(
            Order, Order.id == SettlementDetail.order_id).filter(
            SettlementDetail.settlement_id == pk).all()

        results = {
            'settlement': {
                'id': settlement.id,
                'create_time':
                    settlement.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'start_time':
                    settlement.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time':
                    settlement.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': settlement.status,
                'amount': str(settlement.amount),
                'company_id': company.id,
                'company_name': company.name,
                'xls_oss_url': settlement.xls_oss_url
            }
        }
        l = []
        for row in sets:
            settlement_detail = row[0]
            order = row[1]

            user = db.session.query(UserProfile).filter(
                UserProfile.id == order.user_id).first()

            d = defaultdict()
            d['settlement_detail_id'] = settlement_detail.id
            d['order_id'] = order.id
            d['order_no'] = order.order_no
            d['pay_time'] = order.pay_time.strftime('%Y-%m-%d %H:%M:%S')
            d['amount'] = str(order.amount)
            d['discount'] = str(order.discount)
            d['real_amount'] = str(order.real_amount)
            d['discount_way'] = order.discount_way
            d['user_id'] = order.user_id
            d['user_mobile'] = user.mobile
            l.append(d)
        results['orders'] = l
        return results

    @staticmethod
    def settlement_add(company_id, start_time,
                       end_time, company_pk):
        """
        添加结算
        :param company_id:
        :param start_time:
        :param end_time:
        :param company_pk:
        :return:
        """
        db.session.commit()
        company = db.session.query(Company).filter(
            Company.id == company_pk).first()

        start_time = start_time.strptime('%Y-%m-%d')
        end_time = end_time.strptime('%Y-%m-%d')
        sets = db.session.query(Order, UserProfile, Company).join(
            UserProfile, UserProfile.id == Order.user_id).join(
            Company, Company.id == Order.company_id).filter(
            and_(db.cast(Order.create_time, db.DATE) >= db.cast(start_time, db.DATE),
                 db.cast(Order.create_time, db.DATE) <= db.cast(end_time, db.DATE),
                 Order.company_id == company_pk,
                 Order.status == 2
                 )).all()

        total_amount = Decimal(str(0.0))
        data_details = []
        for row in sets:
            order = row[0]
            user = row[1]
            company = row[2]

            data_details.append({
                'id': order.id,
                'order_no': order.order_no,
                'create_time': order.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'user_mobile': user.mobile,
                'company_name': company.name,
                'amount': order.amount,
                'status': u'成功'
            })
            total_amount += order.amount

        settlement = Settlement()
        settlement.start_time = start_time
        settlement.end_time = end_time
        settlement.status = 1  # 结算完成
        settlement.amount = Decimal(str(total_amount))
        if company_id == 1:
            settlement.company_id = company_pk
        else:
            settlement.company_id = company_id

        data = defaultdict()
        data['file_name'] = '{}-{}'.format(
            settlement.start_time.strftime('%Y-%m-%d'),
            settlement.end_time.strftime('%Y-%m-%d'))
        data['file_data'] = []

        sheet1 = {
            'header': [u'创建时间', u'订单开始时间', u'订单结束时间', u'支付状态',
                       u'公司名称', u'订单总金额'],
            'sheet_name': u'汇总',
            'data': [[settlement.create_time.strftime('%Y-%m-%d'),
                      settlement.start_time.strftime('%Y-%m-%d'),
                      settlement.end_time.strftime('%Y-%m-%d'), u'成功',
                      company.name, settlement.amount]]
        }

        sheet2 = {
            'header': [u'ID', u'订单号', u'创建时间', u'用户手机号',
                       u'公司名称', u'支付金额', u'状态'],
            'sheet_name': u'明细',
            'data': data_details
        }
        data['file_data'].append(sheet1)
        data['file_data'].append(sheet2)

        xls_oss_url = settlement.xls_oss_url = xls.export_xls(data)
        settlement.xls_oss_url = xls_oss_url
        try:
            db.session.add(settlement)
            db.session.flush()
            new_settlement_id = settlement.id
            settlement_detail_objs = []
            for row in sets:
                order = row[0]
                settlement_detail = SettlementDetail()
                settlement_detail.order_id = order.id
                settlement_detail.settlement_id = new_settlement_id
                settlement_detail.company_id = company_id
                settlement_detail_objs.append(settlement_detail)
            db.session.add_all(settlement_detail_objs)
            db.session.commit()
            return {'id': settlement.id}
        except SQLAlchemyError:
            import traceback
            print traceback.format_exc()
            db.session.rollback()
            return -2
        finally:
            db.session.close()

    @staticmethod
    def settlement_filtrate(start_time_str, end_time_str, company_id, offset, limit):
        """结算筛选"""
        from datetime import datetime
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')

        query = db.session.query(Order, UserProfile).join(
            UserProfile, UserProfile.id == Order.user_id).filter(
            Order.company_id == company_id).filter(
            and_(db.cast(Order.scan_time, db.DATE) >= start_time,
                 db.cast(Order.scan_time, db.DATE) <= end_time,
                 Order.company_id == company_id))
        count = query.count()
        sets = query.offset(offset).limit(limit).all()

        total_amount = Decimal(str(0.0))
        discount_amount = Decimal(str(0.0))
        results = []
        for row in sets:
            order = row[0]
            user = row[1]

            d = defaultdict()
            d['id'] = order.id
            d['amount'] = str(order.amount)
            d['discount'] = str(order.discount)
            d['discount_way'] = order.discount_way
            d['order_no'] = order.order_no
            d['pay_time'] = order.pay_time.strftime('%Y-%m-%d %H:%M:%S')
            d['pay_type'] = order.pay_type
            d['real_amount'] = str(order.real_amount)
            d['scan_time'] = order.scan_time.strftime('%Y-%m-%d %H:%M:%S')
            d['status'] = order.status
            d['user_mobile'] = user.mobile
            results.append(d)
            total_amount += Decimal(str(order.amount))
            discount_amount += Decimal(str(order.discount))

        statistics = {
            'order_number': count,
            'time_between': '{}-{}'.format(start_time_str, end_time_str),
            'total_amount': str(total_amount),
            'real_amount': str(total_amount - discount_amount),
            'discount_amount': str(discount_amount)
        }
        return {'count': count, 'results': results, 'statistics': statistics}
