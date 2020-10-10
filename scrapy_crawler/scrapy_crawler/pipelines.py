# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import re

class ScrapyCrawlerPipeline:
    def process_item(self, item, spider):
        if spider.name == 'itcast':
            with open('itcast_teacher.json','a', encoding='utf-8') as f:
                f.write(json.dumps(item, ensure_ascii=False, indent=4))
                f.write('\n')


        if spider.name == 'tencent_hr':
            with open('tencent_hr.json', 'a', encoding='utf-8') as f:
                f.write(json.dumps(item, ensure_ascii=False, indent=4))
                f.write('\n')

        if spider.name == 'suning_books':
            with open('suning_books.json', 'a', encoding='utf-8') as f:
                f.write(json.dumps(item, ensure_ascii=False, indent=4) + '\n')

        return item