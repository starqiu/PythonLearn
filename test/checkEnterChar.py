# -*- coding=utf-8 -*-
import sys
import xlrd
import time
from optparse import OptionParser

reload(sys)
sys.setdefaultencoding('utf8')


def formatExcelColumn(i):
    num = 26  # 字母个数
    m = i % num
    if i < 26 and i >= 0:  # A-Z
        return chr(ord('A') + m)
    elif i >= 26 and i < 26 * 26 + 26:  # AA-ZZ
        i = i / num
        return chr(ord('A') + i - 1) + chr(ord('A') + m)
    else:
        print 'Error: column %d is too large' % i
        return None


def recoverOneChar2Int(ch):  # A-Z 返回0-25
    return ord(ch) - ord('A')


def recoverExcelColumn(colStr):
    num = 26
    if len(colStr) == 1:
        return recoverOneChar2Int(colStr)
    elif len(colStr) == 2:
        return (recoverOneChar2Int(colStr[0]) + 1) * num + recoverOneChar2Int(colStr[1])
    else:
        print 'Error: Excel column String should be A-Z or AA-ZZ'


def needHandle(sheetName):
    # if sheetName != '实体-人':
    #   return False
    if sheetName.find("废弃") >= 0 or sheetName.find("仅目标表") >= 0:
        return False
    elif sheetName.find("实体") != 0 and sheetName.find("事件") != 0 and sheetName.find("关系") != 0:
        return False
    else:
        return True


def main():
    parser = OptionParser()
    parser.add_option("-v", "--viewPath", dest="viewPath", action="store", type="string",
                      help="统一视图的路径")

    if len(sys.argv) <= 1:  # 没有参数时
        parser.print_help()
        return
    options, args = parser.parse_args()
    viewPath = options.viewPath

    print 'deal with view: ' + viewPath
    print '-' * 50

    try:
        xls = xlrd.open_workbook(viewPath)
        sheetNames = xls.sheet_names()
        for sheetName in sheetNames:
            if not needHandle(sheetName):
                continue
            print "开始处理:" + sheetName  # for debug:定位到目标表
            sheet = xls.sheet_by_name(sheetName)
            print 'nrows:%d, ncols:%d' % (sheet.nrows, sheet.ncols)
            for row in range(0, sheet.nrows):
                for column in range(0, sheet.ncols):
                    # print 'row:  %d, column:  %d' % (row, column)
                    value = str(sheet.cell_value(row, column))
                    if '\n' in value or '\r\n' in value:
                        print 'Error: contains \\n . sheetName: %s, Row : %d, Column: %s, value: %s ' % (
                        sheetName, row, formatExcelColumn(column), value.replace('\n', '\\n'))

    except Exception, e:
        print Exception, ":", e, "\n"
        parser.print_help()
        exit(-1)


if __name__ == '__main__':
    print '-' * 50
    start = time.localtime(time.time())
    print time.strftime('%Y-%m-%d %H:%M:%S', start), ' main() start'
    main()
    end = time.localtime(time.time())
    print time.strftime('%Y-%m-%d %H:%M:%S', end), ' main() over'
    print 'costs %f seconds' % (time.mktime(end) - time.mktime(start))
    print '-' * 50
