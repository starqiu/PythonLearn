# -*- coding=utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import json
import sys
import xlrd
import xlwt

style = xlwt.XFStyle()
font = xlwt.Font()
font.name = 'SimSun'  # 指定“宋体”
style.font = font

BaseDicPath = "/program/dic/sources"

try:
    xls = xlrd.open_workbook(sys.argv[1])
    sheetNames = xls.sheet_names()
    # sheet = xls.sheet_by_name("Sheet1")
    sheet = xls.sheet_by_name("SQL Results")
    title = ['TABLE_NAME', 'COMMENTS', 'COLUMN_NAME', 'COMMENTS', 'DATA_TYPE',
             'DATA_LENGTH', 'NULLABLE', 'COLUMN_ID']
    ncols = len(title)

    preTableName = ''
    curTableName = ''

    workbook_t = None
    sheet_t = None

    row_wt = 0
    for row in range(1, sheet.nrows):
        try:
            preTableName = curTableName
            curTableName = sheet.cell_value(row, 1)
            if not preTableName == curTableName:
                row_wt = 0
                # 保存上一张表
                if workbook_t is not None:
                    try:
                        workbook_t.save(BaseDicPath + "/" + preTableName + ".xls")
                    except Exception, e:
                        print Exception, ":", e
                tbNameCn = sheet.cell_value(row, 4)
                if tbNameCn is None or tbNameCn == '':
                    tbNameCn = '未知'
                print 'tbNameCn:', tbNameCn
                workbook_t = xlwt.Workbook(encoding='utf-8')
                sheet_t = workbook_t.add_sheet(tbNameCn, cell_overwrite_ok=True)
                # add title
                for col in range(1, ncols + 1):
                    sheet_t.write(row_wt, col, title[col-1],  style)
            row_wt += 1
            for col in range(1, ncols + 1):
                sheet_t.write(row_wt, col, sheet.cell_value(row, col), style)
        except Exception, e:
            print Exception, ":", e
    # 保存上一张表
    if workbook_t is not None:
        workbook_t.save(BaseDicPath + "/" + preTableName + ".xls")

except Exception, e:
    print Exception, ":", e
    exit(-1)
finally:
    exit(0)
