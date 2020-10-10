# -*- coding: utf-8 -*-
import scrapy
import re

class YanggaungSpider(scrapy.Spider):
    name = 'yangguang'
    allowed_domains = ['sun0769.com']
    start_urls = ['http://wz.sun0769.com/political/index/politicsNewest?id=1&page=1']

    def parse(self, response):
        li_list = response.xpath('//ul[@class="title-state-ul"]/li')
        for li in li_list:
            item = dict()
            item['item_id'] = li.xpath('./span[1]/text()').extract_first()
            item['item_state'] = li.xpath('./span[2]/text()').extract_first()
            item['item_title'] = li.xpath('./span[3]/a/text()').extract_first()
            item['detail_url'] = li.xpath('./span[3]/a/@href').extract_first()
            item['detail_url'] = 'http://wz.sun0769.com/' + item['detail_url']
            item['pub_datetime'] = li.xpath('./span[last()]/text()').extract_first()

            yield scrapy.Request(
                item['detail_url'],
                callback=self.parse_detail,
                meta={'item': item}
            )
        page_num = int(re.findall(r'page_num = parseInt\((.*?)\);', response.body.decode())[0]) if len(re.findall(r'page_num = parseInt(.*?);', response.body.decode())) > 0 else 0
        current_pagenum = int(response.url.split('page=')[-1])
        if current_pagenum < page_num:
            next_page = current_pagenum + 1
            yield scrapy.Request(
                'http://wz.sun0769.com/political/index/politicsNewest?id=1&page={}'.format(next_page),
                callback=self.parse
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['detail'] = response.xpath('//div[@class="details-box"]/pre/text()').extract_first()
        item['img'] = response.xpath('//div[contains(@class,"details-img-list Picture-img")]/img/@src').extract()
        print(item)
