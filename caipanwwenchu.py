# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     caipanwwenchu.py 
   Description :   None
   Author :        LSQ
   date：          2020/9/21
-------------------------------------------------
   Change Activity:
                   2020/9/21: None
-------------------------------------------------
"""
import requests
import execjs
import re
from urllib.parse import urljoin

from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC



# url = 'https://wenshu.court.gov.cn/website/wenshu/181107ANFZ0BXSK4/index.html?docId=ca81a02500e34b868aa8ac380111d2d5'
# headers = {
#     'Cookie': 'HM4hUBT0dDOn443S=cVdefx2weIGvbmH36QTH9Mg0pAQgqT3RuF7aehs2R.vzhgC9IgmaRZBrJXk043HW; SESSION=82f2e22f-b298-44ca-8494-713e644686ff; cna=62DGF9w3BGwCAXFRq2NLDZbo; isg=BHt7DmZcoOoyspxeFhzs6BJXCl_l0I_S3ihQTm04V3qRzJuu9aAfIpkN5myCbOfK; HM4hUBT0dDOn443T=4Dp08HeM7M9JuauNlludqelutE.RqIndGBeyhncIBi28MnVr_vLrtyKvhzwxiQKW5.TDFXRMuMzGAfkUwwxdXC_E9EDm_uooqNIysttalnX_Ou6Crny49IyW1NiFklBJ34HHaA9GYzQYIVysYmZ20v2jkyt5SfxpSdFCQrTVGdghTu5cPmMnhaHCeVAVaIKvqcJbkfX5_vo6Y1BexC98OH1TAy4NNFEqRcUJ0Q5wWyK3gXTJ6HL8MmR6NFyROJkDXG1wIWmklfYTjNYbqwAphKgKeCgzsaH6PNOs_gUWhRkDl8A96w3IAxjlg.3c7TvfM8_bgnJ5_5B21O6E0Pf.CqWNSuvk0M9zCyFj2egxrR12SJV8RHB58953xNhvxpcXLSML',
#     'Host': 'wenshu.court.gov.cn',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
# }
# base_url = 'https://wenshu.court.gov.cn'
# response = requests.get(url, headers=headers).content.decode()
# index_js_url = urljoin(base_url,
#                        re.findall('<script src="(.*?)"></script>', response).pop())
# headers[
#     'Referer'] = 'https://wenshu.court.gov.cn/website/wenshu/181107ANFZ0BXSK4/index.html?docId=ca81a02500e34b868aa8ac380111d2d5'
#
# index_js_code = requests.get(index_js_url, headers=headers).content.decode()
# website_js_url = urljoin(base_url,
#                          re.findall('newscript.setAttribute\("src",.*?"(.*?)"\);', index_js_code, re.DOTALL).pop())
# website_js_code = requests.get(website_js_url, headers=headers).content.decode()
#
# js_code = response + index_js_code + website_js_code
#
# ctx = execjs.compile(js_code)
# rs = ctx.call('getModuleData', '1541573883000')
# print(rs)


# 法律之星
# headers = {
#     'Cookie':'JSESSIONID=E3519EFFF9DDD4ACEA8DB6FA99A72909.alyun1; loginuser=ssmnghunssjust; loginpass=CF9EAE1EDE7880F3D60A5D7C6D84F038',
#     'Referer':'http://law1.law-star.com/law?fn=chl565s566.txt',
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
# }
# resp = requests.get('http://law1.law-star.com/law?fn=chl565s566.txt',headers=headers).content.decode()
# print(resp)