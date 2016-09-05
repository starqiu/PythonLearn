# -*- coding=utf-8 -*-
# ５８同城数据分析与可视化
import sys
from operator import itemgetter
from optparse import OptionParser

import pandas as pd
import numpy as np
import MySQLdb
import time
from datetime import date
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt

reload(sys)
sys.setdefaultencoding('utf8')
matplotlib.rcParams['font.family'] = 'serif'


def autolabel(ax, offset, orient='v'):
    # attach some text labels
    if orient == 'v':
        for rect in ax.patches:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., height + offset, '%0.1f' % height, ha='center', va='bottom')
    else:
        for rect in ax.patches:
            width = rect.get_width()
            ax.text(width + offset, rect.get_y() + rect.get_height() / 2., '%0.1f' % width, ha='left', va='center')


def exec_sql(sql, conn):
    print 'exec sql: %s ' % sql
    conn.query(sql)


# 分析整体均值
def anlysis_all_avg(cur_month, conn):
    data = pd.read_sql_query('select avg(price) as avg from anjuke_ershou_house_%s_%s' % (province, cur_month), conn)
    avg = data['avg'][0]
    print 'avg = %f' % avg
    return avg


# 分析区域均值
def anlysis_area_avg(province, cur_month, conn):
    data = pd.read_sql_query(
            'select area, avg(price) as avg from 58tc_zufang_house_%s_%s GROUP BY area' % (province, cur_month), conn)
    data['area'] = [area.encode('utf8') for area in data['area']]
    data = data.sort_values(by='avg', ascending=False)

    ax = sns.barplot(x=data['area'], y=data['avg'])
    autolabel(ax, 5)
    plt.title(u'区域房价均值')
    plt.xlabel(u"区域area")
    plt.ylabel(u"房价均值avg(单位：元/平方米)")

    plt.legend(loc='best')
    plt.show()

    return data


def get_all_data(province, cur_month, conn):
    data = pd.read_sql_query(
            'select area,town,estate,price  from 58tc_zufang_house_%s_%s limit 1000' % (province, cur_month), conn)
    data['area'] = [area.encode('utf8') for area in data['area']]
    data['town'] = [town.encode('utf8') for town in data['town']]
    data['estate'] = [estate.encode('utf8') for estate in data['estate']]
    return data


def estates_top10(data, price_type='expensive'):
    is_cheap = True if price_type == 'cheap' else False
    data['address'] = data.apply(lambda x: (x.area + x.town + x.estate).encode('utf8'), axis=1)
    estate_price = data[['address', 'price']]
    estate_price = estate_price.groupby('address', as_index=False).agg([np.size, np.mean])
    estate_price = estate_price['price']
    estate_price = estate_price.rename(columns={'mean': 'price'})
    estate_price = estate_price[estate_price['size'] > 3]  # 数据量太少的小区，过滤
    estate_price = estate_price[['price']]
    estate_price = estate_price.sort_values(by='price', ascending=is_cheap)
    estate_price = estate_price[:10]
    ax = sns.barplot(y=estate_price.index, x=estate_price['price'], orient='h')
    autolabel(ax, 15, orient='h')
    plt.title(u'最便宜小区Top 10' if is_cheap else u'最贵小区Top 10')
    plt.xlabel(u"小区")
    plt.ylabel(u"房价均值avg(单位：元/平方米)")

    plt.legend(loc='best')
    plt.show()


parser = OptionParser()
parser.add_option("-w", "--workspace", dest="workspace", action="store", type="string", default='./',
                  help="workspace to store data", metavar="FILE")
parser.add_option("-p", "--province", dest="province", action="store", type="string", default='beijing',
                  help="province that we will crawer")
parser.print_help()
(options, args) = parser.parse_args()

workspace = options.workspace
province = options.province

print 'workspace =%s,  province =%s' % (workspace, province)

cur_month = date.today().strftime('%Y%m')

conn = MySQLdb.connect(host='localhost', user='root', passwd='xing123', db='houses', charset='utf8', port=3306)
# anlysis_all_avg(province, cur_month, conn)
# anlysis_area_avg(province, cur_month, conn)

data = get_all_data(province, cur_month, conn)

estates_top10(data, price_type='cheap')
estates_top10(data, price_type='expensive')

conn.close()
