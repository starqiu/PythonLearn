# -*- coding=utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import json
import sys
import xlrd
import xlwt
from xlutils.copy import copy

style = xlwt.XFStyle()
font = xlwt.Font()
font.name = 'SimSun'  # 指定“宋体”
style.font = font

BaseDicPath = "/program/dic/sources"


def dealwithFile(fileName):
    try:
        xls = xlrd.open_workbook(fileName)
        sheetNames = xls.sheet_names()
        # sheet = xls.sheet_by_name("Sheet1")
        for sheetName in sheetNames:
            try:
                sheetName1 = str(sheetName).upper().replace('SELECT ', '')
                print 'sheetName:' + sheetName1
                if 'SQL' == sheetName1:
                    continue
                workbook = xlrd.open_workbook(BaseDicPath + "/" + sheetName1 + ".xls")
                workbook_t = copy(workbook)
                sheet_t = workbook_t.add_sheet(str('Example'), cell_overwrite_ok=True)
                cur_sheet = xls.sheet_by_name(sheetName)
                for row in range(0, cur_sheet.nrows):
                    for col in range(0, cur_sheet.ncols):
                        sheet_t.write(row, col, cur_sheet.cell_value(row, col), style)

                workbook_t.save(BaseDicPath + "/" + sheetName1 + ".xls")
                print sheetName1, ' gen sucess'
            except Exception, e:
                print Exception, ":", e
    except Exception, e:
        print Exception, ":", e


import os
import os.path
for root, dirs, files in os.walk("/program/dic/example/"):
    for name in files:
        if name.find('~') >= 0:
            continue
        print root + '/' + name
        dealwithFile(root + '/' + name)
# dealwithFile(sys.argv[1])
