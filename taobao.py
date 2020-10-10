# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     taobao.py 
   Description :   None
   Author :        LSQ
   date：          2020/9/3
-------------------------------------------------
   Change Activity:
                   2020/9/3: None
-------------------------------------------------
"""
import time
import splash
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# with Chrome(r'C:\Users\Administrator\Desktop\chromedriver.exe') as browser:
browser = Chrome(r'C:\Users\Administrator\Desktop\chromedriver.exe')
wait = WebDriverWait(browser, 20)
# browser.get('http://www.porters.vip/features/webdriver.html')
# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn.btn-primary.btn-lg')))
# script = 'Object.defineProperty(navigator, "webdriver", { get:() => false, });'
# browser.execute_script(script)
# browser.find_element_by_css_selector('.btn.btn-primary.btn-lg').click()
# elements = browser.find_element_by_id('content')
# time.sleep(1)
# print(elements.text)
browser.get(r'https://login.taobao.com/member/login.jhtml')
