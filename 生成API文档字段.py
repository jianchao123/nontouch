# coding:utf-8
import pymysql

conn = pymysql.connect(
    host='test.wgxing.com',
    user='root',
    password='kIhHAWexFy7pU8qM',
    db='wuganxing_1',
    charset='utf8'
)

api_fields = """
brand,bus_id,bus_load,buy_date,chassis,company_id,engine,load,model_number,product_date,status,type,is_binding,route_id,line_no
"""

cur = conn.cursor()

query_table_sql = "SELECT `COLUMN_NAME`,`DATA_TYPE`," \
                  "`CHARACTER_MAXIMUM_LENGTH` FROM " \
                  "information_schema.COLUMNS WHERE `TABLE_NAME`='{}' " \
                  "AND TABLE_SCHEMA = 'wuganxing_1'"
cur.execute(query_table_sql.format('bus_car'))
fields_raw = cur.fetchall()
model_file = ''

text = ''
for field_row in fields_raw:
    field_name = field_row[0]
    filed_type = field_row[1]

    typee = ''
    if field_name in api_fields:
        if filed_type in ['varchar', 'datetime', 'date', 'text']:
            typee = 'string'
        elif filed_type in ['decimal', 'double']:
            typee = 'number'
        elif 'int' in filed_type:
            typee = 'integer'
        text += '{}:\n  type: {}\n  description: {}\n'.format(field_name, typee, '')
print text
cur.close()
conn.close()

