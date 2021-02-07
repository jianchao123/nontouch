import xlwt
import time
from datetime import datetime
from ext import conf
from utils import oss
"""
{
    file_name:
    file_data:
    [{
        sheet_name:
        header: []
        data
    }]
}
"""


def export_xls(data):

    wb = xlwt.Workbook(encoding='utf-8')

    files = data['file_data']
    for item in files:
        ws = wb.add_sheet(item.get('sheet_name'), '')

        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = item.get('header')

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = item.get('data')
        print "==========================================="
        print rows
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                if isinstance(row[col_num], datetime):
                    ws.write(row_num, col_num, row[col_num].strftime(
                        "%Y-%m-%d %H:%M:%S"), font_style)
                else:
                    ws.write(row_num, col_num, row[col_num], font_style)
    k = str(int(time.time()))
    file_name = conf.config['TEMP_DIR'] + '/' + k
    with open(file_name, 'wb') as fd:
        wb.save(fd)
    oss_key = 'xls/' + k
    oss.upload_local_file(file_name, oss_key + ".xls")
    return 'https://' + conf.config['OSS_BUCKET'] \
           + '.' + conf.config['OSS_POINT'] + '/' + oss_key + ".xls"
