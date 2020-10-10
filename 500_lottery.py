import requests
import json
import re
from lxml import etree


class Lottery(object):
    def __init__(self):
        self.url = 'http://datachart.500.com/dlt/zoushi/newinc/jbzs_foreback.php?expect=all&from={}&to={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Referer': 'http://datachart.500.com/dlt/?expect=all&from={}&to={}'
        }
        self.file = open('lottery.json', 'a', encoding='utf-8')

    def get_response(self, url):
        session = requests.Session()
        response = session.get(url, headers=self.headers)
        return response

    def parse_response(self, response):
        html = etree.HTML(response.content)
        tr_list = html.xpath('//table[@id="chartsTable"]/tr[not(contains(@class, "tdbck"))]')[2:-14]
        for tr in tr_list:
            id = tr.xpath('./td[1]/text()')[0] if len(tr.xpath('./td[1]/text()')) > 0 else None
            red_list = tr.xpath('./td[@class="chartBall01"]/text()')
            blue_list = tr.xpath('./td[@class="chartBall02"]/text()')
            item = dict(id=id, red_list=red_list, blue_list=blue_list)
            self.file.write(json.dumps(item, ensure_ascii=False) + '\n')

    def run(self, start, end):
        # 构造url
        url = self.url.format(start, end)
        self.headers['Referer'] = self.headers['Referer'].format(start, end)
        # 发送请求，获取响应
        response = self.get_response(url)
        # 解析响应，获取并保存数据
        items = self.parse_response(response)


if __name__ == '__main__':
    lottery = Lottery()
    lottery.run('20061', '20061')
    lottery.file.close()
