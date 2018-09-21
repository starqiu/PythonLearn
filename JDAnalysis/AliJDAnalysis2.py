# -*- coding=utf-8 -*-
# 阿里JD（Job Description）分析，查找需要微服务的使用场景
import sys
import json
from bs4 import BeautifulSoup
import time
from datetime import date, datetime
from operator import itemgetter

import requests
import re
import os
from optparse import OptionParser

# from multiprocessing import Pool
# from multiprocessing.dummy import Pool as ThreadPool

reload(sys)
sys.setdefaultencoding('utf8')
# pool = ThreadPool(4)

max_position_id = 99999
zhaopin_home = "https://job.alibaba.com/zhaopin/"
jd_url_patten = "https://job.alibaba.com/zhaopin/position_detail.htm?positionId=%d"
all_path = "F:/jobs/ali/all.json"
new_page_path = "F:/jobs/ali/new/pages/"
new_all_path = "F:/jobs/ali/new/all.json"
new_micro_service_jobs_path = "F:/jobs/ali/new/micro_service_jobs.json"
micro_service_path = "F:/jobs/ali/micro_service.json"
zhaopin_list_action = "https://job.alibaba.com/zhaopin/socialPositionList/doList.json"


def get_JD(jd_url):
    print 'jd_url=' + jd_url
    jd_data = requests.get(jd_url, verify=False, timeout=1)  # SSL连接错误，需要设置verify=False
    soup = BeautifulSoup(jd_data.text)
    jd_one = soup.select_one("div.lf-border-box")
    if jd_one is None or len(jd_one) < 1:
        return None
    else:
        jd_title = jd_one.select_one("h3.bg-title").get_text().replace("  <span> </span>", "")
        # print jd_title
        jd_detail_box = jd_one.select_one("div.detail-box")
        jd_detail_table_td = jd_detail_box.select("table.detail-table.box-border td")
        jd_publish_date = jd_detail_table_td[1].get_text()
        jd_hc = jd_detail_table_td[11].get_text().strip()
        jd_detail_content = jd_detail_box.select("p.detail-content")
        jd_desc = jd_detail_content[0].get_text().strip()
        jd_request = jd_detail_content[1].get_text().strip()
        # jd_content = jd_desc+ jd_request
        jd_content_data = {
            'jd_url': jd_url,
            'jd_title': jd_title,
            'jd_publish_date': jd_publish_date,
            'jd_hc': jd_hc,
            'jd_desc': jd_desc,
            'jd_request': jd_request,
        }

        # print jd_content_data
        return jd_content_data
        # if jd_content.find("微服务")> -1:
        #     return (jd_title,jd_hc,jd_desc,jd_request)

        # jd_publish_time =
        # print jd_publish_date,jd_hc
        # print jd_desc
        # print jd_request
        # jd_hc =
        # print jd_all[0].get_text().replace("  <span> </span>","")


def save_to_file(objs, file_path):
    file_dir = os.path.dirname(file_path)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    print 'save data to %s' % file_path
    jsonData = json.dumps(objs, ensure_ascii=False, indent=4)
    outFile = open(file_path, "w")
    outFile.write(jsonData)
    outFile.close()


def load_from_file(file_path):
    return json.load(open(file_path, 'r'))


def merge_files(small_file_dir, big_file_path):
    big_data = []
    for small_file_path in small_file_dir:
        big_data.append(load_from_file(small_file_path))
    save_to_file(big_data, big_file_path)


def save_all_jds(save_path):
    jd_data_all = []
    for jd_id in range(1, max_position_id):
        jd_data = get_JD(jd_url_patten % jd_id)
        if jd_data is None:
            continue
        jd_data_all.append(jd_data)

    save_to_file(jd_data_all, save_path)


def is_include_mc(desc):
    return desc.find("微服务") > -1


def save_micro_service_jobs():
    all_jobs = load_from_file(all_path)
    micro_service_jobs = []
    for job in all_jobs:
        if is_include_mc(job.get("jd_request")) or is_include_mc(job.get("jd_desc")):
            micro_service_jobs.append(job)
    save_to_file(micro_service_jobs, micro_service_path)


starttime = time.time()


def get_new_jd_by_page(page_id):

    new_page_json_path = new_page_path + str(page_id) + ".json"
    # if page_id == 1:
    #     page_url=zhaopin_home+"position_list.htm"
    # else:
    #     page_url=zhaopin_home+"position_list.htm#page/%d" % page_id
    page_size =10
    # if os.path.exists(new_page_json_path) and get_file_size(house_file_path) == 10:
    #     pass
    page_url = zhaopin_list_action + "?pageSize=%d&t=0.320204139897329&pageIndex=%d" % (page_size, page_id)
    print page_url
    # 该页面先加载静态部分，我们需要的那部分是动态的，不会马上加载。设置stream=True，不会立即下载。see http://docs.python-requests.org/zh_CN/latest/user/advanced.html#advanced
    jd_data_req = requests.post(page_url, verify=False, timeout=1)  # SSL连接错误，需要设置verify=False
    # jd_data.content
    time.sleep(1)
    jd_datas = json.loads(jd_data_req.text).get("returnValue").get("datas")
    save_to_file(jd_datas, new_page_json_path)

    # soup = BeautifulSoup(jd_data.text)
    # jd_url_a_list = soup.select("div.s-list-box > table.table-list > tbody > tr > td > span > a")
    # if jd_url_a_list is None or len(jd_url_a_list) < 1:
    #     return None
    # else:
    #     jd_url_list = [jd_url_a.get("href") for jd_url_a in jd_url_a_list]
    #     return jd_url_a_list
def get_new_jd_by_page_loop(page_id):
    loop = True
    while loop:
        try:
            get_new_jd_by_page(page_id)
            loop = False
        except Exception, e:
            print Exception, ' Error ', e
            time.sleep(60)
# save_all_jds(all_path)
#
# save_micro_service_jobs()
def get_all_new_jd():
    max_page = 634
    for page_id in range(1, max_page + 1):
        get_new_jd_by_page_loop(page_id)

def merge_files(small_file_dir, big_file_path):
    big_data =[]
    small_file_dir = os.path.abspath(small_file_dir)
    small_files = []
    for top, dirs, files in os.walk(small_file_dir):
        if len(dirs) == 0:
            small_files.extend(os.path.join(top, file) for file in files)
    for small_file_path in small_files:
        big_data.extend(load_from_file(small_file_path))
    save_to_file(big_data, big_file_path)


# print get_new_jd_by_page(1)
# get_all_new_jd()

# merge_files(new_page_path, new_all_path)
def get_new_micro_service_jobs():
    new_all_jobs = load_from_file(new_all_path)
    new_micro_service_job = [new_job for new_job in new_all_jobs if is_include_mc(new_job.get("requirement")) or is_include_mc(new_job.get("description"))]
    save_to_file(new_micro_service_job, new_micro_service_jobs_path)

def get_new_micro_service_job_department():
    new_micro_service_job = load_from_file(new_micro_service_jobs_path)
    new_micro_service_job_department = sorted(list(set([j.get("departmentName") for j in new_micro_service_job])))
    # print new_micro_service_job
    save_to_file(new_micro_service_job_department, os.path.dirname(new_micro_service_jobs_path) + "/new_micro_service_job_department.json")

def stat_recruit_number():
    new_all_jobs = load_from_file(new_all_path)
    total_new_recruit_number = reduce(lambda x,y:x+y, [int(new_job.get("recruitNumber")) for new_job in new_all_jobs])
    print total_new_recruit_number

stat_recruit_number()

# if jd is not None:
#     print jd
# jd_micro.append("{}")

# get_JD(jd_url_patten % 1)
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

endtime = time.time()
print 'program cost %f seconds' % (endtime - starttime)
