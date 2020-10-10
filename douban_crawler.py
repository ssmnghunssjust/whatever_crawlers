import requests
import re
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class testSpider(object):
    chromePath = 'C:\\Users\Administrator\Desktop\chromedriver.exe'
    def __init__(self):
        self.url = 'https://www.douyu.com/directory/all'
        self.driver = webdriver.Chrome('C:\\Users\Administrator\Desktop\chromedriver.exe')

    def get_contents(self):
        li_list = self.driver.find_elements_by_class_name('layout-Cover-item')
        contents = []
        for li in li_list:
            title = li.find_element_by_class_name('DyListCover-intro').text
            cate = li.find_element_by_class_name('DyListCover-zone').text
            user = li.find_element_by_class_name('DyListCover-user').text
            hot = li.find_element_by_class_name('DyListCover-hot').text
            item = dict(title=title, cate=cate, user=user, hot=hot)
            contents.append(item)
        return contents

    def save_contents(self, contents):
        with open('douyu.json', 'a', encoding='utf-8') as f:
            for content in contents:
                f.write(json.dumps(content, ensure_ascii=False, indent=4) + '\n')

    def run(self):

        self.driver.get(self.url)
        time.sleep(3)
        contents = self.get_contents()
        self.save_contents(contents)
        next = self.driver.find_element_by_class_name('dy-Pagination-next')
        while True:
            print(next.get_attribute('aria-disabled'))
            if next.get_attribute('aria-disabled') == 'false':
                next.click()
                time.sleep(3)
                contents = self.get_contents()
                self.save_contents(contents)
                next = self.driver.find_element_by_class_name('dy-Pagination-next')
            else:
                break

if __name__ == '__main__':
    myspider = testSpider()
    myspider.run()