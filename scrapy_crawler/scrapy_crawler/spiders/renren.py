# -*- coding: utf-8 -*-
import scrapy


class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com']
    start_urls = ['http://www.renren.com/826906950/newsfeed/photo']

    cookies = 'anonymid=kc0jgtrn-zekkmi; depovince=GW; _r01_=1; JSESSIONID=abcnjojeZ-haI_oWkramx; ick_login=110483b1-e656-48ec-9c21-e04fb6cb822e; taihe_bi_sdk_uid=1b0aa9f14ee1251c7188c66daf4b170e; taihe_bi_sdk_session=7d0a64536c3ffa9303b4e448e456fcb6; jebecookies=f7175780-1d8c-4cb6-91c5-9d6386380f3b|||||; _de=19531429F6455892AA76344FD74CF3E7; p=3b03699018b498a5c5cb2f49f30f96980; first_login_flag=1; ln_uact=13126335602; ln_hurl=http://head.xiaonei.com/photos/0/0/men_main.gif; t=6accfee5cd09497034d6d7078d2366520; societyguester=6accfee5cd09497034d6d7078d2366520; id=826906950; xnsid=ffb8bd0b; loginfrom=syshome'

    cookies = {i.split('=')[0]:i.split('=')[1] for i in cookies.split(';')}

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=self.cookies
        )
    def parse(self, response):
        name = response.xpath('//dl[@class="hd-account clearfix"]/dd//a[@class="hd-name"]/text()').extract_first()
        print(name)
