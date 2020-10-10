# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     jd_spider 
   Description :   None
   Author :        LSQ
   date：          2020/7/24
-------------------------------------------------
   Change Activity:
                   2020/7/24: None
-------------------------------------------------
"""
import requests
import datetime
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'referer': 'https://list.jd.com/list.html?cat=737,794,798&ev=4155_76344&sort=sort_rank_asc&trans=1&JL=2_1_0'
}

url = 'https://list.jd.com/listNew.php?cat=737%2C794%2C798&ev=4155_76344%5E&page=2&s=27&scrolling=y&log_id=1595682605046.9456&tpl=1_M&isList=1&show_items={}'
repsonse = requests.get(
    'https://list.jd.com/listNew.php?cat=737%2C794%2C798&ev=4155_76344%5E&page=1&s=1&click=0',
    headers=headers)
print(datetime.datetime.now(), repsonse.status_code, repsonse.ok)
# print(repsonse.content.decode().find('wids'))
# print(re.findall("wids:'(.*?)',", repsonse.content.decode()))
wids = re.findall("wids:'(.*?)',", repsonse.content.decode())[0]
list_page_2_url = url.format(wids)
resp = requests.get(url.format(wids), headers=headers)
# print(resp.content.decode())
headers['referer'] = list_page_2_url

product_response = requests.get('https://item.jd.com/100005624340.html', headers=headers)
headers['referer'] = 'https://item.jd.com/100005624340.html'

product_price_response = requests.get('https://p.3.cn/prices/mgets?skuIds=J_100005624340', headers=headers)
print('price:%s'%json.loads(product_price_response.content.decode())[0]['p'])
# print(json.loads(product_price_response.content.decode()))
