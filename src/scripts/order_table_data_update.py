# coding:utf-8

from datetime import datetime
import db


class OrderTableDataUpdate(object):

    @db.transaction(is_commit=True)
    def gen(self, mysql_cur):
        """生成五感行公司权限"""
        mysql_db = db.MysqlDbUtil(mysql_cur)
        sql = "SELECT `id`, `permission_name`, `group` FROM `permissions`"
        sets = mysql_db.query(sql)
        d = []
        for row in sets:
            d.append({'permission_id': row[0],
                      'permission_name': row[1],
                      'group': row[2]})
        print json.dumps(d)


import json
if __name__ == '__main__':
    d = OrderTableDataUpdate()
    d.gen()