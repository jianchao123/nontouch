# coding:utf-8
import os
import oss2
import time
import json
import config
import requests
from scripts import db


class ImportPeople(object):
    """导入人员"""

    @db.transaction(is_commit=True)
    def wash_people_data(self):
        """清洗人员数据"""
        mysql_conn = db.MysqlDbUtil(self.mysql_cur)

        import xlrd
        data = xlrd.open_workbook(
            '/home/jianchao/Desktop/人员列表（2020.05.25）.xlsx')
        table = data.sheet_by_index(1)
        print("总行数：" + str(table.nrows))
        print("总列数：" + str(table.ncols))
        for index in range(table.nrows - 1):
            row_data = table.row_values(index + 1)
            emp_no = row_data[0]
            nickname = row_data[1]
            sex = row_data[2]
            id_card = row_data[5]
            mobile = row_data[6]
            department_name = row_data[10]
            if emp_no and nickname and sex and id_card \
                    and mobile and department_name:
                print emp_no, nickname, sex, id_card, mobile, department_name
                d = {
                    '`emp_no`': emp_no,
                    '`nickname`': nickname.encode('utf8'),
                    '`sex`': 1 if sex == u'男' else 2,
                    '`id_card`': id_card,
                    '`mobile`': mobile,
                    '`department_name`': department_name.encode('utf8')
                }
                mysql_conn.insert(d, table_name='`test_people`')

    @db.transaction(is_commit=True)
    def wash_department_data(self):
        mysql_conn = db.MysqlDbUtil(self.mysql_cur)
        import xlrd
        data = xlrd.open_workbook(
            '/home/jianchao/Desktop/人员列表（2020.05.25）.xlsx')
        table = data.sheet_by_index(1)
        print("总行数：" + str(table.nrows))
        print("总列数：" + str(table.ncols))
        d = set([])
        for index in range(table.nrows - 1):
            row_data = table.row_values(index + 1)
            department_name = row_data[10]
            d.add(department_name)
        for row in list(d):
            d = {
                '`name`': row.encode('utf8'),
                '`enterprise_id`': 3,
                '`desc`': (u'西昌钢钒公司-雷诺板材厂-' + row).encode('utf8')
            }
            mysql_conn.insert(d, table_name='`department`')

    @db.transaction(is_commit=True)
    def upload_img(self):
        mysql_conn = db.MysqlDbUtil(self.mysql_cur)
        auth = oss2.Auth(config.OSSAccessKeyId, config.OSSAccessKeySecret)
        bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com',
                             'wgxing-device')

        sql = 'SELECT `id`,`emp_no` FROM `test_people`'
        results = mysql_conn.query(sql)
        directory = u'/home/jianchao/Desktop/人员图片'
        domain = 'http://wgxing-device.oss-cn-beijing.aliyuncs.com/'
        for row in results:
            image_path = directory + '/' + row[1] + ".jpg"
            oss_key = 'people/face/' + row[1] + '.jpg'
            with open(image_path, 'rb') as fd:
                bucket.put_object(oss_key, fd)
            oss_url = domain + oss_key
            d = {
                '`id`': row[0],
                '`oss_url`': oss_url
            }
            mysql_conn.update(d, table_name='`test_people`')

    @db.transaction(is_commit=True)
    def clean(self):
        mysql_conn = db.MysqlDbUtil(self.mysql_cur)
        file_emp_nos = []
        directory = u'/home/jianchao/Desktop/人员图片'
        dirs = os.listdir(directory)
        for row in dirs:
            file_emp_nos.append(row.split('.')[0])

        sql = 'SELECT `emp_no` FROM `test_people`'
        results = mysql_conn.query(sql)
        db_emp_nos = [row[0] for row in results]
        del_str = "'{}'".format("','".join(list(set(db_emp_nos) - set(file_emp_nos))))
        print del_str       # 要删除的数据库记录
        # 清理目录中多余的图片
        for row in list(set(file_emp_nos) - set(db_emp_nos)):
            print os.remove(directory + '/' + row + ".jpg")

    @db.transaction(is_commit=True)
    def generate(self, offset, limit=1000):
        """生成用户"""
        db_trans = db.MysqlDbUtil(self.mysql_cur)
        department_sql = 'SELECT `id`,`name` FROM `department`'
        departments = db_trans.query(department_sql)
        department_data = {}
        for row in departments:
            department_data[row[1]] = row[0]
        print department_data

        sql = 'SELECT `emp_no`,`nickname`,`sex`,`id_card`,' \
              '`mobile`,`department_name`,`oss_url` ' \
              'FROM `test_people` LIMIT {} OFFSET {} '
        results = db_trans.query(sql.format(limit, offset))
        for row in results:
            emp_no = row[0]
            nickname = row[1]
            sex = row[2]
            id_card = row[3]
            mobile = row[4]
            department_name = row[5]
            oss_url = row[6]

            u_data = {
                '`username`': emp_no,
                '`emp_no`': emp_no,
                '`nickname`': nickname.encode('utf8'),
                '`sex`': sex,
                '`mobile`': mobile,
                '`id_card`': id_card,
                '`deadline`': 3169176872,
                '`station_id`': 1,
                '`specified_gps`': '106.423985,30.999503',
                '`address`': '京都xxxx',
                '`is_internal_staff`': 1,
                '`create_time`': 'now()'
            }
            db_trans.insert(u_data, table_name='`user_profile`')
            user_pk = db_trans.get("SELECT `id` FROM `user_profile` WHERE `emp_no`='{}'".format(emp_no))[0]
            f_data = {
                '`oss_url`': oss_url,
                '`status`': 1,
                '`nickname`': nickname.encode('utf8'),
                '`user_id`': user_pk,
                '`emp_no`': emp_no
            }
            db_trans.insert(f_data, table_name='`face`')
            r_data = {
                '`user_id`': user_pk,
                '`role_id`': 3
            }
            db_trans.insert(r_data, table_name='`user_role_relation`')

            d = {
                '`user_id`': user_pk,
                '`department_id`': department_data[department_name]
            }
            db_trans.insert(d, table_name='`user_department_relation`')

    def test(self):
        import time
        start = time.time()
        OSSDomain = 'https://wgxing-device.oss-cn-beijing.aliyuncs.com'
        OSSAccessKeyId = 'LTAIWE5CGeOiozf7'
        OSSAccessKeySecret = 'IGuoRIxwMlPQqJ9ujWyTvSq2em4RDj'
        OSSEndpoint = 'oss-cn-beijing.aliyuncs.com'
        OSSBucketName = 'wgxing-device'
        self.auth = oss2.Auth(OSSAccessKeyId, OSSAccessKeySecret)
        self.bucket = oss2.Bucket(self.auth, OSSEndpoint,
                                  OSSBucketName)

        oss_face = []
        for obj in oss2.ObjectIterator(self.bucket, prefix='people/face/'):
            slash_arr = obj.key.split("/")
            if slash_arr and len(slash_arr) == 3:
                comma_arr = slash_arr[-1].split('.')
                if comma_arr and len(comma_arr) == 2 and comma_arr[-1] == 'jpg':
                    oss_face.append(comma_arr[0])
        oss_face_set = set(oss_face)

        server_face_list = sorted(['123456789', '0000008', '0000216', '0000232', '0000278', '0000293', '0000316', '0000324', '0000337', '0000351', '0000378', '0000444', '0000523', '0000530', '0000658', '0000672', '0000710', '0000720', '0000734'])
        server_face_set = set(server_face_list)
        intersection = oss_face_set & server_face_set
        intersection = sorted(list(intersection))
        print intersection
        print server_face_list
        end = time.time()
        print end - start


if __name__ == '__main__':
    import_people = ImportPeople()
    import_people.test()
    #import_people.wash_people_data()
    #import_people.wash_department_data()
    #import_people.upload_img()
    #import_people.generate(12999)




# select * from test_people where emp_no in( select emp_no from test_people group by emp_no having count(*)>1)
