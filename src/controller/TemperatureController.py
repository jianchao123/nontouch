# coding:utf-8

from flask.blueprints import Blueprint
from core.framework import get_require_check_with_permissions
from service.TemperatureService import TemperatureService

try:
    import requests

    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

# """蓝图对象"""
bp = Blueprint('TemperatureController', __name__)
"""蓝图url前缀"""
url_prefix = '/api_backend/v1'


@bp.route('/temperature/list', methods=['GET'])
@get_require_check_with_permissions([])
def temperature_list(user_id, company_id, args):
    """
    温度列表
    """
    offset = int(args['offset'])
    limit = int(args['limit'])
    return TemperatureService.temperature_list(company_id, 0, 0)