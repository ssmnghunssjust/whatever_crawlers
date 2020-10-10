# -*- coding: utf-8 -*-
import scrapy
import json
from copy import deepcopy
from scrapy_redis.spiders import RedisSpider

class TencentHrSpider(scrapy.Spider):
    name = 'tencent_hr'
    allowed_domains = ['tencent.com']
    start_urls = ['https://careers.tencent.com/tencentcareer/api/post/Query?pageIndex=1&pageSize=10&area=cn']

    # redis_key = 'tencent_hr'

    start_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?pageIndex={}&pageSize=10&area=cn'
    # 获取详情页的json数据
    detail_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?postId={}'
    # 点击链接打开详情页
    detail_web_url = 'http://careers.tencent.com/jobdesc.html?postId={}'
    pageIndex = 1

    def parse(self, response):
        item = dict()
        base_json = json.loads(response.body.decode())
        post_list = base_json['Data']['Posts']
        recruit_count = base_json['Data']['Count']
        for post in post_list:
            item['post_id'] = post.get('PostId',None)
            item['招聘岗位'] = post.get('RecruitPostName',None)
            item['国家'] = post.get('CountryName',None)
            item['城市'] = post.get('LocationName',None)
            item['职责'] = post.get('Responsibility',None)
            item['详情链接'] = self.detail_web_url.format(item['post_id'])
            item['更新日期'] = post.get('LastUpdateTime',None)

            yield scrapy.Request(
                self.detail_url.format(item['post_id']),
                callback=self.parse_detail,
                meta={'item': deepcopy(item)}
            )
            if self.pageIndex < recruit_count / 10:
                self.pageIndex += 1
                print('current_page:%d'%self.pageIndex)
                yield scrapy.Request(
                    self.start_url.format(self.pageIndex),
                    callback=self.parse
                )

    def parse_detail(self, response):
        detail_json = json.loads(response.body.decode())
        detail_data_dict = detail_json['Data']
        item = response.meta['item']
        item['岗位要求'] = detail_data_dict['Requirement']
        yield item
