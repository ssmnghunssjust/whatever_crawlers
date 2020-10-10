# -*- coding: utf-8 -*-
import scrapy
import re
import json
from copy import deepcopy

class SuningBooksSpider(scrapy.Spider):
    name = 'suning_books'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/?safp=d488778a.homepage1.99345513004.47&safpn=10001']

    cookies = '_snsr=direct%7Cdirect%7C%7C%7C; districtId=10326; cityId=9048; _snvd=1593333461151hXFjrh+r1ud; tradeMA=194; streetCode=7520199; cityCode=752; hm_guid=15c6930c-80d9-4b9b-8f35-c0a6006fc9d4; _df_ud=906eae70-eed6-4cee-8fb8-60726c08c1c6; SN_SESSION_ID=3807aaa6-ff1b-4383-bf73-e78fd666734e; sesab=ACBAABC; sesabv=3%2C12%2C16%2C1%2C2%2C8%2C3; SN_CITY=190_752_1000048_9048_01_10326_1_1_99_7520199; _device_session_id=p_42980c1e-8a58-4b56-8980-d958998528a8; _cp_dt=86e51b24-8297-4f78-9253-80cb3ae06a03-84930; _snzwt=TH5Yil172fe22b6deF2vp739c; smhst=696718474|0070138369a698933098|0070138369a11660693694|0071062099a11002227902|0070067633a11883012858|0071151794; authId=siBCA2E68DC3A5BF2517EDB6ECDB3E65CA; _snmc=1; _snms=159340866770564121; _snma=1%7C159333346101536747%7C1593333461015%7C1593408667685%7C1593408698450%7C38%7C6; _snmp=159340869805049604; _snmb=159340855339488541%7C1593408698471%7C1593408698455%7C7; token=59f781b0-9f1f-4948-9c6f-ed9542ace98c'
    cookies = {i.split('=')[0]:i.split('=')[1] for i in cookies.split(';')}
    def parse(self, response):
        first_cate_div_list = response.xpath('//div[@class="menu-list"]/div[@class="menu-item"]')
        for i, div in enumerate(first_cate_div_list, 1):
            item = dict()
            item['first_cate']=div.xpath('./dl/dt/h3/a/text()').extract_first()
            second_cate_p_list = response.xpath('//div[@class="menu-list"]/div[@class="menu-sub"]['+str(i)+']//div[@class="submenu-left"]/p')
            for j, p in enumerate(second_cate_p_list, 1):
                item['second_cate'] = p.xpath('./a/text()').extract_first()
                third_cate_li_list = response.xpath('//div[@class="menu-list"]/div[@class="menu-sub"]['+str(i)+']//div[@class="submenu-left"]/ul['+str(j)+']/li')
                for li in third_cate_li_list:
                    item['third_cate']=li.xpath('./a/text()').extract_first()
                    item['cate_url']=li.xpath('./a/@href').extract_first()
                    item['cate_id']= re.findall('-(.*?)-', item['cate_url'])[0]
                    yield scrapy.Request(
                        item['cate_url'],
                        callback=self.parse_list,
                        meta={'item':deepcopy(item)},
                        cookies=self.cookies
                    )

    def parse_list(self, response):
        item = response.meta['item']
        book_li_list = response.xpath('//div[@id="filter-results"]/ul/li')
        print('book_li_list长度:',len(book_li_list))
        for li in book_li_list:
            item['sell_point'] = li.xpath('.//div[@class="res-info"]//p[@class="sell-point"]/a/text()').extract_first()
            item['product_url'] = 'https:' + li.xpath('.//div[@class="res-info"]//p[@class="sell-point"]/a/@href').extract_first()
            # sa_data = li.xpath('.//p[@class="com-cnt"]/a[last()]/@sa-data').extract_first()
            # sa_data = {i.split(':')[0]:i.split(':')[1] for i in sa_data.split(',')}
            # product_id = sa_data.get('prdid')
            onclick = li.xpath('.//p[@class="com-cnt"]/a[last()]/@onclick').extract_first()
            shop_id = re.findall('javascript:addToInterests\(\'(.*?)-', onclick)[0]
            partNumber = re.findall(',\'(.*?)\',this\)', onclick)[0]
            product_json_url = 'http://pas.suning.com/nspcsale_0_'+partNumber+'_'+partNumber+'_'+shop_id+'_190_752.html'
            item['product_json_url'] = product_json_url
            yield scrapy.Request(
                product_json_url,
                callback=self.parse_product,
                meta={'item':deepcopy(item)},
                cookies=self.cookies
            )
            totalPage_span = response.xpath('//div[@id="bottom_pager"]//span[@class="page-more"]/text()').extract_first()
            totalPage = int(re.findall('共(.*?)页',totalPage_span)[0])
            currentPage = int(response.xpath('//a[@class="cur"]/text()').extract_first())
            nextPage = currentPage + 1
            if currentPage < totalPage - 1:
                yield scrapy.Request(
                    'https://list.suning.com/' + str(nextPage),
                    callback=self.parse_list,
                    meta={'item': deepcopy(item)}
                )

    def parse_product(self, response):
        item = response.meta['item']
        response_dict = re.findall('pcData\((.*?)\)', response.body.decode())[0]
        response_json = json.loads(response_dict)['data']
        item['price'] = response_json['price']['saleInfo'][0]['netPrice']
        # print(item)
        yield item