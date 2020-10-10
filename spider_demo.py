import requests
import re
import json
import logging
from lxml import etree

class Spider_name(object):
    def __init__(self):
        self.url = ''
        self.headers = {
            'User-Agent': '',
            'Referer': ''
        }
        self.fp = open('file_name', 'a', encoding='utf-8')

    def get_response(self,url):
        session = requests.session()
        response = session.get(url, headers=self.headers)
        logger = logging.getLogger(__name__)
        logger.log(20, 'getting response from %s'%url)
        return response

    def parse_response(self,response):
        html = etree.HTML(response.content)
        return html

    def get_content(self,html):
        #html.xpath()
        pass


    def run(self):
        # 1.构造第一个url
        url = self.url.format()
        # 2.发送请求，获取响应
        response = self.get_response(url)
        # 3.从响应中提取数据（也可以保存数据）
        html = self.parse_response()
        # 4.保存数据
        self.get_content()
        # 5.构造下一个url地址

        # 6.重复步骤2至5


if __name__ == '__main__':
    spider = Spider_name()
    spider.run()