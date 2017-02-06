# -*- coding=utf-8 -*-
import sys
import xlrd
import time
import re
from optparse import OptionParser
import MySQLdb

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


def getAttrTypeDic(cur, tableName):
    queryStr = 'select a.attr_name,a.column_type from origin_table t, origin_attr a where t.origin_table_id=a.origin_table_id and t.tb_name_en=\'%s\'' % (
        tableName)
    # print queryStr
    cur.execute(queryStr)
    results = cur.fetchall()
    dic = {}
    for res in results:
        dic[res[0]] = res[1]
    return dic


def getOriginTableName(originTableNameAll):  # '常驻人口信息(htlx_t_rk_czrk_jbxx)(监护人2)'=>'htlx_t_rk_czrk_jbxx'
    originTableNameAll = originTableNameAll.replace('）', ')').replace('（', '(')
    return originTableNameAll.replace(')', '').split('(')[1].strip().upper()


def getOriginAttrName(originAllNameAll):  # 'JHREHM(null)'=>'JHREHM'
    return originAllNameAll.split('(')[0].strip();


def getBracketOutIn(i):  # 获取括号外和括号内的字符串
    i = str(i)
    start = i.find("(")
    finish = i.find(")")
    if start == -1 or finish == -1:
        return i, "ERROR"
    else:
        outVal = i[0:start]
        inVal = i[start + 1:finish]
        return outVal, inVal


def getRuleStartRow(sheet):
    ruleStartRow = 1
    for i in range(5, sheet.nrows):
        if sheet.cell_value(i, 0) == "" and sheet.cell_value(i, 1) == "" and sheet.cell_value(i, 3) == "":  # 检查是不是末尾的注释行
            ruleStartRow = i  # 得到规则开始的行号
            break
    return ruleStartRow


def getTargetTimeTypeIndex(sheet):
    timeTpyeRowIndexArray = []
    for row in range(5, sheet.nrows):
        dataType = sheet.cell_value(row, 5)
        if dataType == "Date" or dataType == "Time":
            timeTpyeRowIndexArray.append(row)
    return timeTpyeRowIndexArray


def isMustHandledDataSource(sheet, column):
    if sheet.cell_value(0, column) == "priority" or sheet.cell_value(0, column) == '':  # 检查是不是优先级列或是无效列
        return False
    datasource = "oracle"
    if sheet.cell_value(2, column) != "":
        datasource = sheet.cell_value(2, column)
    mustHandledDatasouces = ['', 'oracle', 'oracle1', 'oracle2']  # 只处理网安(暂不)和Oracle数据源,''为Oracle数据源
    if datasource not in mustHandledDatasouces:
        # print 'DataSource: %s ignore!' % sheet.cell_value(2,j)
        return False
    return True

def dealFunc(funcStr,needStat=True):  # "hello_1 = fff_a(a, b_1)"=>('hello','hello_1','fff_a','a, b_1'),是否需要统计计数？
    try:
        m = re.match('(.*)\s*=\s*(.*)', funcStr)
        outputName = m.group(1).strip()
        funcAndParams = m.group(2).strip()
        m = re.match('(.*)\((.*)\)', funcAndParams)
        func = m.group(1).strip()
        params = m.group(2).strip()
        m = re.match('(.*)_\d+', outputName)
        targetAttrName = m.group(1).strip()
    except Exception, e:
        print Exception, " Error: ", e
        return ('', '', '', '')
    return (targetAttrName, outputName, func, params)

def getAllRulesInMapping(sheet, column, ruleStartRow):
    allRulesInMapping = []
    # print 'ruleStartRow:%d' % ruleStartRow
    if ruleStartRow == 1:  # 没有规则
        print 'sheet: %s has not rules' % sheet.sheet_name
        return allRulesInMapping
    # 遍历一个映射下的所有规则
    for row in range(ruleStartRow, sheet.nrows):
        if sheet.cell_value(row, column).strip() == "":  # 该单元格没有规则
            continue
        allRulesInMapping.append(sheet.cell_value(row, column).strip())
    return allRulesInMapping


def getTimeRuleTargetAttrAndParamsMap(allRulesInMapping):
    timeRuleTargetAttrAndParamsMap = {}
    for rule in allRulesInMapping:
        (targetAttrName, outputName, func, params) = dealFunc(rule)
        if func == 'time_2_long':
            timeRuleTargetAttrAndParamsMap[targetAttrName] = params
    return timeRuleTargetAttrAndParamsMap


def main():
    parser = OptionParser()
    parser.add_option("-v", "--viewPath", dest="viewPath", action="store", type="string", metavar="FILE",
                      help="统一视图的路径")
    parser.add_option("-o", "--host", dest="host", action="store", type="string", default="k1222.mlamp.co",
                      help="主机名或ip")
    parser.add_option("-d", "--database", dest="database", action="store", type="string", default="cona",
                      help="数据库名")
    parser.add_option("-u", "--user", dest="user", action="store", type="string", default="cona",
                      help="用户名")
    parser.add_option("-p", "--password", dest="password", action="store", type="string", default="cona",
                      help="密码")
    parser.add_option("-t", "--port", dest="port", action="store", type="int", default=3306,
                      help="端口")
    parser.add_option("-w", "--workspace", dest="workspace", action="store", type="string", default=".",
                      metavar="DIRECTORY",
                      help="工作目录")
    parser.add_option("-s", "--StartSrcTable", dest="StartSrcTable", action="store", type="int", default='18',
                      help="起始的原始表的列，若统一视图加了列，则该数据需要变动")

    if len(sys.argv) <= 1:  # 没有参数时
        parser.print_help()
        return
    options, args = parser.parse_args()
    print options
    workspace = options.workspace
    viewPath = options.viewPath
    host = options.host
    database = options.database
    user = options.user
    password = options.password
    port = options.port
    StartSrcTable = options.StartSrcTable  # 起始的原始表的列，若统一视图加了列，则该数据需要变动

    print 'deal with view: ' + viewPath
    print '-' * 50

    # CHAR,VCHAR,LONGVCHAR,NVCHAR,NCHAR
    allStringType = [1, 12, -1, -9, -15]

    try:
        conn = MySQLdb.connect(host=host, user=user, passwd=password, db=database, charset='utf8',
                               port=port)
        cur = conn.cursor()
        xls = xlrd.open_workbook(viewPath)
        sheetNames = xls.sheet_names()
        needQueryTableAndField = [] # (table,field)
        # print '%-40s,%-30s,%-30s' % ('sheetName', 'tableName', 'originAttrName')
        for sheetName in sheetNames:
            if not needHandle(sheetName):
                continue
            print "开始处理:" + sheetName  # for debug:定位到目标表
            sheet = xls.sheet_by_name(sheetName)
            print 'nrows:%d, ncols:%d' % (sheet.nrows, sheet.ncols)

            timeTpyeRowIndexArray = getTargetTimeTypeIndex(sheet)
            if len(timeTpyeRowIndexArray) == 0:  # 目标表没有时间列
                continue

            ruleStartRow = getRuleStartRow(sheet)

            for column in range(StartSrcTable, sheet.ncols):
                if not isMustHandledDataSource(sheet, column):
                    continue
                else:
                    allRulesInMapping = getAllRulesInMapping(sheet, column, ruleStartRow)

                    tableName = getOriginTableName(sheet.cell_value(0, column))
                    dic = getAttrTypeDic(cur, tableName)
                    if len(dic) == 0:  # 没有属性
                        continue
                    for timeRow in timeTpyeRowIndexArray:
                        if sheet.cell_value(timeRow, column) == "":  # 原表中没有与该时间列对应的列，不处理
                            continue
                        else:
                            originAttrName = getOriginAttrName(sheet.cell_value(timeRow, column))
                            targetAttrName = sheet.cell_value(timeRow, 1)
                            timeRuleTargetAttrAndParamsMap = getTimeRuleTargetAttrAndParamsMap(allRulesInMapping)
                            if not timeRuleTargetAttrAndParamsMap.has_key(targetAttrName):
                                print 'Error: lack of time Rule in: sheet(%s), originTable(%s), Row(%d), Column(%s)' % (sheetName, tableName, timeRow, formatExcelColumn(column))
                                continue
                            # print 'sheet(%s), Row(%d), Column(%s)' % (sheetName, timeRow, formatExcelColumn(column))
                            params = timeRuleTargetAttrAndParamsMap[targetAttrName]
                            paramsSize = len(params.split(','))
                            column_type = dic[originAttrName]
                            if column_type in allStringType and paramsSize != 2:  # 原表中与时间列对应的列在Oracle中是String类型
                                # print '%-40s,%-30s,%-30s' % (sheetName, tableName, originAttrName)
                                print 'Error: error apply time_2_long rule, data type of %s is String, please check sheet(%s), originTable(%s), Row(%d), Column(%s) ' \
                                      % (originAttrName, sheetName, tableName, timeRow, formatExcelColumn(column))
                                needQueryTableAndField.append('(TABLE_NAME='+tableName+'AND COLUMN_NAME='+originAttrName+')')
                            elif column_type not in allStringType and paramsSize != 1:
                                print 'Error: error apply time_2_long rule, data type of %s is Time, please check sheet(%s), originTable(%s), Row(%d), Column(%s) ' \
                                      % (originAttrName, sheetName, tableName, timeRow, formatExcelColumn(column))
                                needQueryTableAndField.append('(TABLE_NAME=\''+tableName+'\' AND COLUMN_NAME=\''+originAttrName+'\')')
                            else:
                                pass
            print "处理成功:" + sheetName + "\n"

        if len(needQueryTableAndField) > 0:
            sql = 'SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE  FROM user_tab_columns WHERE' + ' OR '.join(needQueryTableAndField) + ';'
            print 'Please input this sql to query the data type of field in Oracle:\n' + sql

    except Exception, e:
        print Exception, ":", e, "\n"
        parser.print_help()
        exit(-1)
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    print '-' * 50
    start = time.localtime(time.time())
    print time.strftime('%Y-%m-%d %H:%M:%S', start), ' main() start'
    main()
    end = time.localtime(time.time())
    print time.strftime('%Y-%m-%d %H:%M:%S', end), ' main() over'
    print 'costs %f seconds' % (time.mktime(end) - time.mktime(start))
    print '-' * 50
