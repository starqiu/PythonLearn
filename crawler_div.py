# -*- coding=utf-8 -*-
# 将网页中的某一块内容保存成本地html以便复制
import sys
from bs4 import BeautifulSoup

import requests

reload(sys)
sys.setdefaultencoding('utf8')

def save_remote_div_text_2_local_html(url, selctor, file="output1.html", encoding="utf-8"):

    content = requests.get(url)
    # infoencode = chardet.detect(content).get('encoding', 'utf-8')
    # print "infoencode=", infoencode
    content.encoding = encoding
    soup = BeautifulSoup(content.text, features="html.parser")
    res_data = soup.select(selctor)
    with open(file, "w") as f:
        map(lambda data: f.write(str(data)), res_data)
    # res_text = map(lambda data: data.get_text(separator="\n"), res_data)
    # return res_data[0]

save_remote_div_text_2_local_html("https://www.4paradigm.com/product/prophet", "ul#accordion > li:nth-of-type(4)")
