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
    if l > other_dis_start_index and l % 2 == 1:
        # 花色 和 点数
        huase_dianshu = zip(card_data_info_text_list[other_dis_start_index::2], card_data_info_text_list[other_dis_start_index + 1::2])
        other_dis = map(lambda (x, y): x.strip() + y.strip(), huase_dianshu)
        dis.extend(other_dis)

    elif l == other_dis_start_index:
        pass
    else:
        print "Error: l = %d , should >= %d and be odd" % (l, other_dis_start_index)

    return dis

def get_card_info_by_url(card_url, card_type):
    whole_url = MAIN_PAGE + card_url
    print "whole_url = ", whole_url
    card_data = requests.get(whole_url)
    # !!! 此处保证不乱码,查看whole_url网页源代码的header,看看使用了哪种编码方式。
    card_data.encoding="gb2312"
    soup = BeautifulSoup(card_data.text, features="html.parser")
    # table 中的第一个tr中的第二个td
    card_info = {}
    # if whole_url.find("jibenpai") > -1 or  whole_url.find("jibenpai") > -1:
    if card_type == "game": # 如果是游戏牌,需要将卡牌分布合并成一个list(一个杀对应多张卡牌),武将牌不存在一对多的关系
        card_data_info_list = soup.select("table tr td div  span")
        card_data_info_text_list = map(lambda card_data_info: card_data_info.get_text().strip(), card_data_info_list)
        # 去除空格(&nbsp)
        card_data_info_text_list = [c for c in card_data_info_text_list if c != ""]
        distribte_start_index = -1
        for (i, data) in enumerate(card_data_info_text_list):
            if data.find("卡牌分布：") > -1:
                distribte_start_index = i
        for i in range(0, distribte_start_index, 2):
            card_info[card_data_info_text_list[i]] = card_data_info_text_list[i+1]
        card_info["卡牌分布："] = get_distribute(card_data_info_text_list, distribte_start_index)
    else:
        card_data_info_list = soup.select("table tr td div span")
        card_data_info_text_list = map(lambda card_data_info: card_data_info.get_text().strip(), card_data_info_list)
        # 去除空格(&nbsp)
        card_data_info_text_list = [c for c in card_data_info_text_list if c != ""]
        card_info={
            "武将名称：": card_data_info_text_list[2],
            "武将编号：": card_data_info_text_list[6],
            "武将称号：": card_data_info_text_list[10],
            "国籍：": card_data_info_text_list[14],
            "体力上限：": card_data_info_text_list[18],
            "武将技：": card_data_info_text_list[20],
        }
        # for i in range(0, len(card_data_info_text_list), 2):
        #     card_info[card_data_info_text_list[i]] = card_data_info_text_list[i+1]
    card_info["url"] = whole_url
    # save_to_file(card_info, "data/card_info")
    return card_info

def get_all_card_info_list(card_url_list, card_type):
    # 其他卡牌(野心家) 不算基本卡牌
    card_url_list_filer = [u for u in card_url_list if u.find("qita") < 0 ]
    return map(lambda card_url: get_card_info_by_url(card_url, card_type), card_url_list_filer)

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

starttime = time.time()

# 1. 获取所有的卡牌
# game_card_url_list = get_all_game_card_url_list()
# save_to_file(game_card_url_list, "data/game_card_url_list")
# print card_url_list
# 2. 获取说有的卡牌详细信息
# get_game_card_info_by_url("/a/kapaiyilan/youxipai/zhuangbeipai/2013/0128/127.html", "game")
# game_card_url_list_from_file = load_from_file("data/game_card_url_list")
# game_card_info_list = get_all_game_card_info_list(game_card_url_list_from_file, "game")
# save_to_file(game_card_info_list, "data/game_card_info_list")
# 3. 获取所有的武将牌
# forces_card_url_list = get_all_forces_card_url_list()
# save_to_file(forces_card_url_list, "data/forces_card_url_list")
# 4. 获取所有的武将牌信息
# forces_card_url_list_from_file = load_from_file( "data/forces_card_url_list")
# forces_card_info_list = get_all_card_info_list(forces_card_url_list_from_file, "wujiang")
# save_to_file(forces_card_info_list, "data/forces_card_info_list")

endtime = time.time()
print 'program cost %f seconds' % (endtime - starttime)