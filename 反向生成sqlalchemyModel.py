# coding:utf-8
import pymysql

text = """# coding:utf-8\nfrom db import db\n\n\nclass {object_name}(db.Model):\n\t__tablename__ = '{table_name}'\n
"""

conn = pymysql.connect(
    host='test.wgxing.com',
    user='root',
    password='kIhHAWexFy7pU8qM',
    db='wuganxing',
    charset='utf8'
)

cur = conn.cursor()
sql = "select TABLE_NAME from information_schema.COLUMNS " \
      "where TABLE_SCHEMA = 'wuganxing' GROUP BY `TABLE_NAME`"
cur.execute(sql)
table_names = [field[0] for field in cur.fetchall()]
print "所有表名"
print table_names
query_table_sql = "SELECT `COLUMN_NAME`,`DATA_TYPE`," \
                  "`CHARACTER_MAXIMUM_LENGTH` FROM " \
                  "information_schema.COLUMNS WHERE `TABLE_NAME`='{}' " \
                  "AND TABLE_SCHEMA = 'wuganxing'"
for table_name in table_names:
    arr = table_name.split("_")
    if len(arr) > 1:
        table_name_hump = ''
        for x in arr:
            table_name_hump += x.capitalize()
        #table_name_hump = '{}{}'.format(arr[0].capitalize(), arr[1].capitalize())
    else:
        table_name_hump = table_name.capitalize()
    model_file = text.format(object_name=table_name_hump, table_name=table_name)
    cur.execute(query_table_sql.format(table_name))
    fields_raw = cur.fetchall()
    print fields_raw
    for field_row in fields_raw:
        field_name = field_row[0]
        filed_type = field_row[1]
        field_len = str(field_row[2])
        if field_name == 'id':
            model_file += "\tid = db.Column(db.BigInteger, primary_key=True)\n"
        else:
            field_type_fmt = None
            field_len_fmt = None
            if filed_type == 'varchar':
                field_type_fmt = 'String'
                field_len_fmt = '(' + field_len + ')'
            elif 'datetime' == filed_type:
                field_type_fmt = 'DateTime'
                field_len_fmt = ', default=datetime.now'
            elif 'decimal' == filed_type:
                field_type_fmt = 'Numeric'
                field_len_fmt = '(11, 6)'
            elif 'date' == filed_type:
                field_type_fmt = 'Date'
                field_len_fmt = ''
            elif 'double' == filed_type:
                field_type_fmt = 'Numeric'
                field_len_fmt = '(11, 6)'
            elif 'int' in filed_type:
                field_type_fmt = 'Integer'
                field_len_fmt = ''
            elif 'text' in filed_type:
                field_type_fmt = 'Text'
                field_len_fmt = '()'
            else:
                print field_name, filed_type, field_len
            if field_type_fmt:
                model_file += "\t{} = db.Column(db.{}{})\n".format(field_name, field_type_fmt, field_len_fmt)
    print model_file
    fd = open('./ttmp/{}.py'.format(table_name_hump), 'w')
    fd.write(model_file)
    fd.close()

cur.close()
conn.close()