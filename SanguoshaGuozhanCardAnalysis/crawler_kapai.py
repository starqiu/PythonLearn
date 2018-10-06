# -*- coding=utf-8 -*-
# 三国杀国战卡牌爬虫
import sys
import json
from bs4 import BeautifulSoup
import time
from datetime import date, datetime
from operator import itemgetter

import requests
# import pandas
# import MySQLdb
import re
import os
from optparse import OptionParser


reload(sys)
sys.setdefaultencoding('utf8')

MAIN_PAGE="http://guozhan.sanguosha.com/"

"""
获取所有的卡牌地址
"""
def get_all_game_card_url_list():
    main_page_data = requests.get(MAIN_PAGE)
    soup = BeautifulSoup(main_page_data.text, features="html.parser")
    # soup.select("")

    card_a_list = soup.select("div#game_card .game_center li > a" )
    card_url_list = map(lambda card_a: card_a.get("href"), card_a_list)
    return card_url_list

"""
获取所有的武将牌地址
"""
def get_all_forces_card_url_list():
    main_page_data = requests.get(MAIN_PAGE)
    soup = BeautifulSoup(main_page_data.text, features="html.parser")
    card_a_list = soup.select("div#forces_card .forces_center li > a" )
    card_url_list = map(lambda card_a: card_a.get("href"), card_a_list)
    return card_url_list


"""
乱码字符串转成中文
"""
def str2chinese(s):
    print type(s)
    return s.encode('gb2312')

def f(x):
    print(json.dumps(x, ensure_ascii=False))
    x

def get_distribute(card_data_info_text_list, dis_start_index):
    dis = list()
    l = len(card_data_info_text_list)
    other_dis_start_index = dis_start_index + 1
    if l < dis_start_index:
        return dis
    first_dis = card_data_info_text_list[dis_start_index].replace("卡牌分布：","").strip()

    if first_dis != "":
        dis.append(first_dis)
    if  l > other_dis_start_index and l % 2 == 1:
        # 花色 和 点数
        huase_dianshu = zip(card_data_info_text_list[other_dis_start_index::2], card_data_info_text_list[other_dis_start_index + 1::2])
        other_dis = map(lambda (x,y): x.strip()+y.strip(), huase_dianshu)
        dis.extend(other_dis)

    elif l == other_dis_start_index:
        pass
    else:
        print "Error: l = %d , should >= %d and be odd" % (l, other_dis_start_index)

    return dis

def get_game_card_info_by_url(card_url):
    whole_url = MAIN_PAGE + card_url
    print "whole_url = ", whole_url
    card_data = requests.get(whole_url)
    # !!! 此处保证不乱码,查看whole_url网页源代码的header,看看使用了哪种编码方式。
    card_data.encoding="gb2312"
    soup = BeautifulSoup(card_data.text, features="html.parser")
    # table 中的第一个tr中的第二个td
    card_info = {}
    if whole_url.find("jibenpai") > -1 or  whole_url.find("jibenpai") > -1:
        card_data_info_list = soup.select("table tr:nth-of-type(1) td:nth-of-type(2) > div > span")
        card_data_info_text_list = map(lambda card_data_info: card_data_info.get_text().replace("【|】","").strip(), card_data_info_list)
        card_info = {
            "name": card_data_info_text_list[1], # 卡牌名称
            "type": card_data_info_text_list[3], # 卡牌种类
            "chance": card_data_info_text_list[5], # 出牌时机
            "target": card_data_info_text_list[7], # 使用目标
            "effect": card_data_info_text_list[9], # 使用效果
            "num": card_data_info_text_list[11], # 卡牌数量
            "distribute": get_distribute(card_data_info_text_list, 12), # 卡牌分布
        }
    elif whole_url.find("zhuangbeipai") > -1:
        card_data_info_list = soup.select("table tr:nth-of-type(2) td > div > span")
        card_data_info_text_list = map(lambda card_data_info: card_data_info.get_text().replace("【|】","").strip(), card_data_info_list)
        # 去除空格(&nbsp)
        card_data_info_text_list = [c for c in card_data_info_text_list if c != ""]
        card_info = {
            "name": card_data_info_text_list[1], # 卡牌名称
            "type": card_data_info_text_list[3], # 卡牌种类
            "effect": card_data_info_text_list[5], # 使用效果
            "num": card_data_info_text_list[7], # 卡牌数量
            "distribute": get_distribute(card_data_info_text_list, 8), # 卡牌分布
        }
    else:
        print "ERROR, wrong URL"
    save_to_file(card_info, "data/card_info")
    return card_info

def get_all_game_card_info_list(card_url_list):
    # 其他卡牌(野心家) 不算基本卡牌
    card_url_list_filer = [u for u in card_url_list if u.find("qita") < 0 ]
    return map(lambda card_url: get_game_card_info_by_url(card_url), card_url_list_filer)


#
# def get_areas(url_province):
#     province_data = requests.get(url_province)
#     soup = BeautifulSoup(province_data.text)
#     areas_a = soup.select("div.div-border.items-list > div > span.elems-l > a")
#     areas_obj = []
#     for area_a in areas_a:
#         obj = {
#             "url": area_a.get("href"),
#             "address": area_a.get_text()
#         }
#         areas_obj.append(obj)
#     return areas_obj
#
#
# def get_towns_by_area(area_obj):
#     area_data = requests.get(area_obj.get('url'))
#     soup = BeautifulSoup(area_data.text)
#     towns_a = soup.select("div#game_card.items-list > div > span.elems-l > div.sub-items > a")
#     towns_obj = []
#     for town_a in towns_a:
#         obj = {
#             'url': town_a.get('href'),
#             'town': town_a.get_text(),
#             'area': area_obj.get('address')
#         }
#         towns_obj.append(obj)
#     return towns_obj
#
#
# def get_towns_by_province(province):
#     print 'start to crawle data,province = ' + province
#
#     url_province = 'http://%s.58tc.com/sale/' % province
#     areas_obj = get_areas(url_province)
#     towns = []
#     for area_obj in areas_obj:
#         towns.extend(get_towns_by_area(area_obj))
#
#     print 'the number of towns in %s : %d' % (province, len(towns))
#
#     return towns
#
#
def save_to_file(objs, file_path):
    file_dir = os.path.dirname(file_path)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    print 'save data to %s' % file_path
    jsonData = json.dumps(objs, ensure_ascii=False, indent=4)
    outFile = open(file_path, "w")
    outFile.write(jsonData)
    outFile.close()

def load_from_file(json_path):
    return json.load(open(json_path, 'r'))


# def crawlerTowns(province, cur_month, workspace='./'):
#     towns = get_towns_by_province(province)
#     towns_file_path = '%s/%s/towns/%s.json' % (workspace, cur_month, province)
#     save_to_file(towns, towns_file_path)
#
#
# def get_houses_by_town(town):
#     # o5表示按最新排序，取前50页，每页60条
#     time.sleep(1)
#     houses = []
#     for page_no in range(1, 51):
#         url = '%s/o5-p%d' % (town.get('url'), page_no)
#         print 'start to crawler url: %s' % url
#         web_data = requests.get(url)
#         soup = BeautifulSoup(web_data.text)
#         house_details = soup.select('div.sale-left > ul.houselist-mod > li.list-item > div.house-details')
#         for house_detail in house_details:
#             try:
#                 price = house_detail.select('div.details-item > span')[2].get_text()
#                 address = house_detail.select('div.details-item > span.comm-address')[0].get_text()
#                 house_data = {
#                     'price': int(re.match('(\d+).*', price).group(1)),
#                     'estate': address.encode().split("\xc2\xa0\xc2\xa0")[0].strip(),  # 小区
#                     'town': town.get('town'),
#                     'area': town.get('area')
#                 }
#                 houses.append(house_data)
#             except Exception, e:
#                 print price, address
#                 print Exception, " Error: ", e
#     return houses
#
#
# def crawler_houses(workspace, towns_file_path):
#     towns = json.loads(open(towns_file_path, 'r').read(-1))
#     total = len(towns)
#     i = 0
#     for town in towns:
#         i += 1
#         print 'start to deal with town:%s , progress: %d/%d '% (town, i, total)
#         house_file_path = '%s/%s/houses/%s/%s/%s.json' % (workspace, cur_month, province, town.get('area'), town.get('town'))
#         if os.path.exists(house_file_path) and get_file_size(house_file_path) > 100:
#             continue
#
#         houses = get_houses_by_town(town)
#         save_to_file(houses, house_file_path)
#
#
# def get_file_size(path):
#     st = os.lstat(path)
#     return st.st_size
#
#
# # 确保超时后还可以继续执行，反反爬虫
# def crawler_houses_with_loop(workspace, towns_file_path):
#     loop = True
#     while loop:
#         try:
#             crawler_houses(workspace, towns_file_path)
#             loop = False
#         except Exception, e:
#             print Exception, ' Error ', e
#             time.sleep(60)
#
#
# def exec_sql(sql, conn):
#     print 'exec sql: %s ' % sql
#     conn.query(sql)
#
#
# def init_table(province, cur_month, conn):
#     exec_sql('drop table if exists 58tc_zufang_house_%s_%s' % (province, cur_month), conn)
#     exec_sql(
#         'create table 58tc_zufang_house_%s_%s (id INT PRIMARY KEY AUTO_INCREMENT,area VARCHAR(30), town VARCHAR(30),estate VARCHAR(40),price INT)' % (province, cur_month),
#         conn)
#     exec_sql('alter table 58tc_zufang_house_%s_%s AUTO_INCREMENT=1' % (province, cur_month), conn)
#
#
# def load_house_json_to_db(house_json_path, cur_month, conn):
#     houses = json.load(open(house_json_path, 'r'))
#     if len(houses) == 0:
#         return
#     head = 'insert into 58tc_zufang_house_%s_%s (area,town,estate,price) VALUES ' % (province, cur_month)
#     values = []
#     for house in sorted(houses, key=itemgetter('estate')):
#         values.append('(\'%s\',\'%s\',\'%s\',%d)' % (
#         house.get('area'), house.get('town'), house.get('estate'), house.get('price')))
#     sql = head + ','.join(values)
#     exec_sql(sql, conn)
#     conn.commit()
#
#
# def get_house_json_array(province, cur_month, workspace='./'):
#     workspace = os.path.abspath(workspace)
#     root_dir = '%s/%s/houses/%s' % (workspace, cur_month, province)
#     root_dir = root_dir.replace('//', '/')
#     all_house_json_files = []
#     for top, dirs, files in os.walk(root_dir):
#         if len(dirs) == 0:
#             all_house_json_files.extend(os.path.join(top, file) for file in files)
#             # print all_house_json_files
#     return all_house_json_files
#
#
# def load_all_houses_into_db(province, cur_month, workspace, conn):
#     all_house_json_files = get_house_json_array(province, cur_month, workspace)
#     for house_json in all_house_json_files:
#         print 'start to load file : %s' % house_json
#         load_house_json_to_db(house_json, cur_month, conn)
#
#
# def load_data_into_db(province, cur_month, workspace):
#     conn = MySQLdb.connect(host='localhost', user='root', passwd='xing123', db='houses', charset='utf8', port=3306)
#     init_table(province, cur_month, conn)
#     load_all_houses_into_db(province, cur_month, workspace, conn)
#     conn.close()
#
# parser = OptionParser()
# parser.add_option("-w", "--workspace", dest="workspace", action="store", type="string", default='./',
#                   help="workspace to store data", metavar="FILE")
# parser.add_option("-p", "--province", dest="province", action="store", type="string", default='beijing',
#                   help="province that we will crawer")
# parser.add_option("-t", "--crawler_towns", dest="crawler_towns", action="store_true", default=False,
#                   help="crawler towns")
# parser.add_option("-c", "--crawler_houses", dest="crawler_houses", action="store_true", default=False,
#                   help="crawler towns")
# parser.add_option("-l", "--load", dest="load_data_into_db", action="store_true", default=False,
#                   help="load data into db")
#
# (options, args) = parser.parse_args()
#
# workspace = options.workspace
# province = options.province
#
# print 'workspace =%s,province =%s' % (workspace, province)
#
# cur_month = date.today().strftime('%Y%m')
starttime = time.time()

# # 1. crawler towns
# if options.crawler_towns:
#     crawlerTowns(province, cur_month, workspace=workspace)
#
# # 2. crawler house source
# if options.crawler_houses:
#     towns_file_path = '%s/%s/towns/%s.json' % (workspace, cur_month, province)
#     crawler_houses_with_loop(workspace, towns_file_path)
#
# # 3. write data into database
# if options.load_data_into_db:
#     load_data_into_db(province, cur_month, workspace)


# 1. 获取所有的卡牌
# game_card_url_list = get_all_game_card_url_list()
# save_to_file(game_card_url_list, "data/game_card_url_list")
# print card_url_list
# 2. 获取说有的卡牌详细信息
get_game_card_info_by_url("/a/kapaiyilan/youxipai/zhuangbeipai/2013/0128/127.html")
game_card_url_list_from_file = load_from_file("data/game_card_url_list")
game_card_info_list = get_all_game_card_info_list(game_card_url_list_from_file)
save_to_file(game_card_info_list, "data/game_card_info_list")
# 3. 获取所有的武将牌
# forces_card_url_list = get_all_forces_card_url_list()
# save_to_file(forces_card_url_list, "data/forces_card_url_list")
# 4. 获取所有的武将牌信息
# forces_card_url_list_from_file = load_from_file( "data/forces_card_url_list")
# forces_card_info_list = get_all_card_info_list(forces_card_url_list_from_file)
endtime = time.time()
print 'program cost %f seconds' % (endtime - starttime)