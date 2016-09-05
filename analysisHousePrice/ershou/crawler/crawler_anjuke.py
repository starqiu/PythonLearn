# -*- coding=utf-8 -*-
# 安居客爬虫
import sys
import json
from bs4 import BeautifulSoup
import time
from datetime import date, datetime
from operator import itemgetter

import requests
import pandas
import MySQLdb
import re
import os
from optparse import OptionParser
# from multiprocessing import Pool
# from multiprocessing.dummy import Pool as ThreadPool

reload(sys)
sys.setdefaultencoding('utf8')
# pool = ThreadPool(4)



def get_areas(url_province):
    province_data = requests.get(url_province)
    soup = BeautifulSoup(province_data.text)
    areas_a = soup.select("div.div-border.items-list > div > span.elems-l > a")
    areas_obj = []
    for area_a in areas_a:
        obj = {
            "url": area_a.get("href"),
            "address": area_a.get_text()
        }
        areas_obj.append(obj)
    return areas_obj


def get_towns_by_area(area_obj):
    area_data = requests.get(area_obj.get('url'))
    soup = BeautifulSoup(area_data.text)
    towns_a = soup.select("div.div-border.items-list > div > span.elems-l > div.sub-items > a")
    towns_obj = []
    for town_a in towns_a:
        obj = {
            'url': town_a.get('href'),
            'town': town_a.get_text(),
            'area': area_obj.get('address')
        }
        towns_obj.append(obj)
    return towns_obj


def get_towns_by_province(province):
    print 'start to crawle data,province = ' + province

    url_province = 'http://%s.anjuke.com/sale/' % province
    areas_obj = get_areas(url_province)
    towns = []
    for area_obj in areas_obj:
        towns.extend(get_towns_by_area(area_obj))

    print 'the number of towns in %s : %d' % (province, len(towns))

    return towns


def save_to_file(objs, file_path):
    file_dir = os.path.dirname(file_path)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    print 'save data to %s' % file_path
    jsonData = json.dumps(objs, ensure_ascii=False, indent=4)
    outFile = open(file_path, "w")
    outFile.write(jsonData)
    outFile.close()


def crawlerTowns(province, cur_month, workspace='./'):
    towns = get_towns_by_province(province)
    towns_file_path = '%s/%s/towns/%s.json' % (workspace, cur_month, province)
    save_to_file(towns, towns_file_path)


def get_houses_by_town(town):
    # o5表示按最新排序，取前50页，每页60条
    time.sleep(1)
    houses = []
    for page_no in range(1, 51):
        url = '%s/o5-p%d' % (town.get('url'), page_no)
        print 'start to crawler url: %s' % url
        web_data = requests.get(url)
        soup = BeautifulSoup(web_data.text)
        house_details = soup.select('div.sale-left > ul.houselist-mod > li.list-item > div.house-details')
        for house_detail in house_details:
            try:
                price = house_detail.select('div.details-item > span')[2].get_text()
                address = house_detail.select('div.details-item > span.comm-address')[0].get_text()
                house_data = {
                    'price': int(re.match('(\d+).*', price).group(1)),
                    'estate': address.encode().split("\xc2\xa0\xc2\xa0")[0].strip(),  # 小区
                    'town': town.get('town'),
                    'area': town.get('area')
                }
                houses.append(house_data)
            except Exception, e:
                print price, address
                print Exception, " Error: ", e
    return houses


def crawler_houses(workspace, towns_file_path):
    towns = json.loads(open(towns_file_path, 'r').read(-1))
    total = len(towns)
    i = 0
    for town in towns:
        i += 1
        print 'start to deal with town:%s , progress: %d/%d '% (town, i, total)
        house_file_path = '%s/%s/houses/%s/%s/%s.json' % (workspace, cur_month, province, town.get('area'), town.get('town'))
        if os.path.exists(house_file_path) and get_file_size(house_file_path) > 100:
            continue

        houses = get_houses_by_town(town)
        save_to_file(houses, house_file_path)


def get_file_size(path):
    st = os.lstat(path)
    return st.st_size


# 确保超时后还可以继续执行，反反爬虫
def crawler_houses_with_loop(workspace, towns_file_path):
    loop = True
    while loop:
        try:
            crawler_houses(workspace, towns_file_path)
            loop = False
        except Exception, e:
            print Exception, ' Error ', e
            time.sleep(60)


def exec_sql(sql, conn):
    print 'exec sql: %s ' % sql
    conn.query(sql)


def init_table(province, cur_month, conn):
    exec_sql('drop table if exists anjuke_ershou_house_%s_%s' % (province, cur_month), conn)
    exec_sql(
        'create table anjuke_ershou_house_%s_%s (id INT PRIMARY KEY AUTO_INCREMENT,area VARCHAR(30), town VARCHAR(30),estate VARCHAR(40),price INT)' % (province, cur_month),
        conn)
    exec_sql('alter table anjuke_ershou_house_%s_%s AUTO_INCREMENT=1' % (province, cur_month), conn)


def load_house_json_to_db(house_json_path, cur_month, conn):
    houses = json.load(open(house_json_path, 'r'))
    if len(houses) == 0:
        return
    head = 'insert into anjuke_ershou_house_%s_%s (area,town,estate,price) VALUES ' % (province, cur_month)
    values = []
    for house in sorted(houses, key=itemgetter('estate')):
        values.append('(\'%s\',\'%s\',\'%s\',%d)' % (
        house.get('area'), house.get('town'), house.get('estate'), house.get('price')))
    sql = head + ','.join(values)
    exec_sql(sql, conn)
    conn.commit()


def get_house_json_array(province, cur_month, workspace='./'):
    workspace = os.path.abspath(workspace)
    root_dir = '%s/%s/houses/%s' % (workspace, cur_month, province)
    root_dir = root_dir.replace('//', '/')
    all_house_json_files = []
    for top, dirs, files in os.walk(root_dir):
        if len(dirs) == 0:
            all_house_json_files.extend(os.path.join(top, file) for file in files)
            # print all_house_json_files
    return all_house_json_files


def load_all_houses_into_db(province, cur_month, workspace, conn):
    all_house_json_files = get_house_json_array(province, cur_month, workspace)
    for house_json in all_house_json_files:
        print 'start to load file : %s' % house_json
        load_house_json_to_db(house_json, cur_month, conn)


def load_data_into_db(province, cur_month, workspace):
    conn = MySQLdb.connect(host='localhost', user='root', passwd='xing123', db='houses', charset='utf8', port=3306)
    init_table(province, cur_month, conn)
    load_all_houses_into_db(province, cur_month, workspace, conn)
    conn.close()

parser = OptionParser()
parser.add_option("-w", "--workspace", dest="workspace", action="store", type="string", default='./',
                  help="workspace to store data", metavar="FILE")
parser.add_option("-p", "--province", dest="province", action="store", type="string", default='beijing',
                  help="province that we will crawer")
parser.add_option("-t", "--crawler_towns", dest="crawler_towns", action="store_true", default=False,
                  help="crawler towns")
parser.add_option("-c", "--crawler_houses", dest="crawler_houses", action="store_true", default=False,
                  help="crawler towns")
parser.add_option("-l", "--load", dest="load_data_into_db", action="store_true", default=False,
                  help="load data into db")

(options, args) = parser.parse_args()

workspace = options.workspace
province = options.province

print 'workspace =%s,province =%s' % (workspace, province)

cur_month = date.today().strftime('%Y%m')
starttime = time.time()

# 1. crawler towns
if options.crawler_towns:
    crawlerTowns(province, cur_month, workspace=workspace)

# 2. crawler house source
if options.crawler_houses:
    towns_file_path = '%s/%s/towns/%s.json' % (workspace, cur_month, province)
    crawler_houses_with_loop(workspace, towns_file_path)

# 3. write data into database
if options.load_data_into_db:
    load_data_into_db(province, cur_month, workspace)

endtime = time.time()
print 'program cost %f seconds' % (endtime - starttime)