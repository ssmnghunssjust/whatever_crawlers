# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_crawler.items import ScrapyCrawlerItem

class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        li_list = response.xpath('//div[@class="tea_con"]/div/ul/li')
        item = ScrapyCrawlerItem()
        for li in li_list:
            item['name'] = li.xpath('./div[2]//h3/text()').extract_first()
            item['title'] = li.xpath('./div[2]//h4/text()').extract_first()
            item['desc'] = li.xpath('./div[2]//p/text()').extract_first()
            item['img'] = li.xpath('./div[1]/img/@data-original').extract_first()
            if item['img'] is not None:
                item['img'] = 'http://www.itcast.cn/' + item['img']
            yield dict(item)