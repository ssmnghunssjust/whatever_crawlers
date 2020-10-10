# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     wechat_gongzhong.py 
   Description :   None
   Author :        LSQ
   date：          2020/9/9
-------------------------------------------------
   Change Activity:
                   2020/9/9: None
-------------------------------------------------
"""
import requests
import time
import json
import re
import os
import random
import logging
import sys
from lxml.etree import HTML, tostring
from pymongo import MongoClient


class OfficialAccount(object):
    def __init__(self, nickname=None, fakeid=None, official_cookie=None, official_token=None, appmsg_token=None,
                 wechat_cookie=None, begin_page=0):
        self.nickname = nickname
        self.official_cookie = official_cookie
        self.official_token = official_token
        self.appmsg_token = appmsg_token
        self.wechat_cookie = wechat_cookie
        self.begin_page = begin_page
        self.logger = self.get_logger('wechat_gongzhong.log')
        if not os.path.exists(self.nickname):
            os.mkdir(self.nickname)
        self.fp = open(os.path.join(self.nickname, 'articles.json'), 'a', encoding='utf-8')
        self.mongo_client = MongoClient('mongodb://127.0.0.1:27017')
        self.collection = self.mongo_client['wechat_gongzhong'][self.nickname]
        if not fakeid is None:
            self.fakeid = fakeid
        else:
            self.logger.exception('必须提供一个公众号的fakeid')
            raise Exception('必须提供一个公众号的fakeid')

    def __del__(self):
        self.fp.close()
        self.mongo_client.close()

    def get_logger(self, filename=None):
        logger = logging.getLogger(__name__)
        formatter = logging.Formatter(fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        file_handler = logging.FileHandler(filename, encoding='utf-8')
        stream_handler_stdout = logging.StreamHandler(sys.stderr)
        file_handler.setFormatter(formatter)
        stream_handler_stdout.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler_stdout)
        logger.setLevel(logging.INFO)
        return logger

    def __get_all_articles(self):
        index = self.begin_page
        begin = (self.begin_page - 1) * 5
        while True:
            # print('正在获取第%s页文章列表' % index)
            self.logger.info('正在获取第%s页文章列表' % index)
            articles_sum, page_articles = self.__get_page_articles(begin)
            begin += 5
            index += 1
            yield page_articles
            if begin >= articles_sum:
                break
            time.sleep(5)

    def __get_page_articles(self, begin=0):
        url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'cookie': self.official_cookie,
            'referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&createType=0&token=1110913688&lang=zh_CN'
        }
        params = {
            'action': 'list_ex',
            'begin': begin,
            'count': '5',
            'fakeid': self.fakeid,
            'type': '9',
            'query': '',
            'token': self.official_token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
        }
        articles = list()
        content_json = requests.get(url, headers=headers, params=params).json()
        if content_json.get('base_resp', {}).get('err_msg', None) != 'ok':
            self.logger.exception(f'无法获取文章列表，可能遭遇反爬!\n{content_json}')
            raise Exception(f'无法获取文章列表，可能遭遇反爬!\n{content_json}')
        for item in content_json.get('app_msg_list'):
            article = dict()
            article['title'] = item.get('title', None)
            # bson.errors.InvalidDocument: key '粤剧进校园丨深大校园传来悠扬的唱腔？那是......' must not contain '.'
            if article['title'] is not None:
                article['title'] = article['title'].replace('.', '').replace('$', '')
            article['copyright'] = item.get('copyright_type', None)
            article['link'] = item.get('link', None)
            articles.append(article)
        return content_json.get('app_msg_cnt'), articles

    def __get_article_info(self, article=None):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
            'Cookie': self.wechat_cookie,
            # 'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
            'Host': 'mp.weixin.qq.com',
        }
        # 获取文章内容
        content_html = requests.get(article.get('link'), headers=headers).content.decode()
        # 订正文章内容，将<img>标签的src替换为正常url链接
        html = HTML(content_html)
        img_list = html.xpath('//img[@data-src]')
        for img in img_list:
            data_src = img.xpath('./@data-src').pop()
            img_html_old = tostring(img).decode()
            img.set('src', data_src)
            img_html_new = tostring(img).decode()
            content_html = content_html.replace(img_html_old, img_html_new)
        content_html = content_html.replace(
            'item.src = "data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg=="',
            'item.src = item.getAttribute("data-src")')
        # re提取文章的发布时间
        publish_time = re.findall('t=".*?",n=".*?",s="(.*?)";', content_html)
        if publish_time:
            publish_time = publish_time.pop()
        else:
            publish_time = re.findall('<span id="publish_time">(.*?)</span>', content_html).pop()
        filename = article.get('title')
        filename = re.sub(r'[/\\:\*\?"<>|;]', '_', filename)
        filename = filename.replace(' ', '')
        filename = filename + '_' + publish_time + '_' + str(round(time.time() * 1000))
        filename = os.path.join(os.path.dirname(__name__), self.nickname, filename)
        with open(filename + '.html', 'w', encoding='utf-8') as f:
            f.write(content_html)

        if '此内容发送失败无法查看' in content_html:
            return content_html, {}, {}

        # 获取查询字符串信息
        msg_link = re.findall(
            r'var msg_link = "http://mp.weixin.qq.com/s\?__biz=(.*?)&amp;mid=(.*?)&amp;idx=(.*?)&amp;sn=(.*?)&amp',
            content_html)
        if msg_link:
            biz, mid, idx, sn = msg_link.pop()
        else:
            biz, mid, idx, sn = re.findall(
                r'<meta property="og:url" content="http://mp.weixin.qq.com/s\?__biz=(.*?)&amp;mid=(.*?)&amp;idx=(.*?)&amp;sn=(.*?)&amp',
                content_html).pop()
        is_only_read = re.findall('var is_only_read = "1" \* (.*?);', content_html)
        if not is_only_read:
            is_only_read = re.findall('d.is_only_read = "1" \* (.*?);', content_html).pop()

        is_temp_url = re.findall('var is_temp_url = "" \? 1 : (.*?);', content_html)
        if not is_temp_url:
            is_temp_url = re.findall('d.is_temp_url = "" \? 1 : (.*?);', content_html).pop()

        appmsg_type = re.findall('var appmsg_type = "(.*?)";', content_html)
        if not appmsg_type:
            appmsg_type = re.findall('_g.appmsg_type = "(.*?)";', content_html).pop()

        comment_id = re.findall(r'var comment_id = "(.*?)" \|\|', content_html)
        if not comment_id:
            comment_id = re.findall(r'd.comment_id = "(.*?)";', content_html).pop()
        # key = re.findall("var key = '(.*?)';", content_html).pop()
        # pass_ticket = re.findall("var pass_ticket = '(.*?)';", content_html).pop()
        # appmsg_token = re.findall('var appmsg_token\s*= "(.*?)";', content_html).pop()
        # appmsgid = re.findall(r'var appmsgid = "" \|\| \'\' \|\| \'(.*?)\';', content_html).pop()

        data = {
            'is_only_read': is_only_read,
            'is_temp_url': is_temp_url,
            'appmsg_type': appmsg_type,
            '__biz': biz,
            'mid': mid,
            'sn': sn,
            'idx': idx,
        }

        # 获取文章的阅读量、点赞量、在看量、评论数量
        article_info_url = 'https://mp.weixin.qq.com/mp/getappmsgext?'
        article_info_url = article_info_url + "appmsg_token={}&x5=0".format(self.appmsg_token)
        time.sleep(random.random())
        article_info_json = requests.post(article_info_url, headers=headers, data=data).json()
        if article_info_json.get('appmsgstat', None) is None:
            raise Exception('appmsg_token或wechat_cookie已过期，无法获取文章阅读量、点赞量等信息，请使用fiddler并从微信客户端点击一篇文章，获取响应必要数据')
        query_params = {
            'action': 'getcomment',
            '__biz': biz,
            'idx': idx,
            'comment_id': comment_id,
            'limit': '100',
        }
        # 获取文章的评论信息，包括评论id、评论内容、评论者名称、评论点赞数量，是否评论置顶
        comments_url = 'https://mp.weixin.qq.com/mp/appmsg_comment'
        time.sleep(random.uniform(1, 2))
        comments_json = requests.get(comments_url, headers=headers, params=query_params).json()

        return content_html, article_info_json, comments_json

    def run(self):
        # 实现程序主逻辑
        # 基于页数的文章列表生成器，用于获取每一页的文章列表，列表中每个元素都是字典，字典中包含文章内容、文章阅读量、点赞量等信息和文章评论
        articles = self.__get_all_articles()

        # 获取所有文章的相关信息
        # 遍历文章列表生成器，获取每一页的文章列表
        for page_articles in articles:
            # 遍历文章列表，获取每个文章的所有信息
            for article in page_articles:
                article_title = article.get('title')
                article_dict = dict()
                article_dict[article_title] = dict()
                content_html, article_info_json, comments_json = self.__get_article_info(article)
                # articles_dict[article_title]['content_html'] = content_html
                article_dict[article_title]['article_info_json'] = article_info_json
                article_dict[article_title]['comments_json'] = comments_json
                self.fp.write(json.dumps(article_dict, indent=4, ensure_ascii=False))
                count = self.collection.count_documents({'_id': article_title})
                if count == 0:
                    article_dict['_id'] = article_title
                    self.collection.insert_one(article_dict)
                    self.logger.info('成功写入文章：%s' % article_title)
                else:
                    self.logger.warning('文章*****“%s”*****已存在数据库中！' % article_title)
                # print('成功写入文章：%s' % article_title)
                time.sleep(random.uniform(5, 10))


if __name__ == '__main__':
    nickname = '深圳大学'
    # 登录公众平台，发布图文，从超链接处获取fakeid和official_token和official_cookie
    fakeid = 'MzA5MzYwNjA4MQ=='
    official_token = '1552089153'
    # official_cookie = 'appmsglist_action_3896466306=card; ua_id=Plf3lhpcGuv9m4K6AAAAADOfgjClZ-Mz3LSTjE4JKi4=; pgv_pvi=1331574784; openid2ticket_oLuIc5MVg0Zulj1z7pjK4Mq0vRJs=; mm_lang=zh_CN; pgv_pvid=172926700; openid2ticket_oTQ_25YIAYrrlcCyvLO7mRvoPqg8=; pgv_si=s6177298432; openid2ticket_ogls_6Jj6NFF48wSygfQL-wIrAs4=; rewardsn=; wxtokenkey=777; cert=WG6SIMyTQWXBcO51xVVEyQdGlkmtlFh0; master_key=CtZLycfOvjGoGqcaYJAGF498eqn5NQ8txnxJscLVqOg=; pgv_info=ssid=s3215716391; media_ticket=c89d9d40f6959f02438f855efef690f65e200d2b; media_ticket_id=gh_3ea2769d6f16; wxuin=99791591857567; sig=h01d13d26e3b0a0115172394129f2b9c5525417cb1d4c52a79da24712cc3eaf43e627675bfcc05bd1c5; uuid=bf2e63def45e1583ae7af90bc3dc5061; rand_info=CAESIMywqRFz3XOdtvzL2D3y82ndtLLG6cTq0AmrtZFyoA7Z; slave_bizuin=3896466306; data_bizuin=3896466306; bizuin=3896466306; data_ticket=W5Xxmf5GNu9zBy9Xw2zjly5DCza11bMAtUBdaUuVtVcMHQk+SAax6lhW376BgQGf; slave_sid=QllEYlp1RVI4QlNhck5zMnBnRzJoZ045cG4xVm9GYmdSa0k4b1FzN3hZcXNKdDgyQjVoMVdLQkFHMXNmR19fU2xwaU1LVGJkakdSWVNxNzlER0NMYWd1VmFzaGxtVzRxSlpCTVB4YXB0OWNHRHo0anZ2bUx3ODJGRGwxdjJEMDdIaFRZQ1lPWDRnNWJJNkJh; slave_user=gh_d604d5e48427; xid=c01da42d27190c53e339314a2202ebc1'
    # 深圳大学公众号的cookie
    official_cookie = 'appmsglist_action_3896466306=card; ua_id=Plf3lhpcGuv9m4K6AAAAADOfgjClZ-Mz3LSTjE4JKi4=; pgv_pvi=1331574784; openid2ticket_oLuIc5MVg0Zulj1z7pjK4Mq0vRJs=; mm_lang=zh_CN; pgv_pvid=172926700; openid2ticket_oTQ_25YIAYrrlcCyvLO7mRvoPqg8=; openid2ticket_ogls_6Jj6NFF48wSygfQL-wIrAs4=; wxuin=99791591857567; pgv_si=s2552370176; uuid=8809b5f014c06aa8f3f56915aebed01e; rand_info=CAESIJ81QMFo5rZWaGNf3NkMrYZMvUC73jG6jJX2oVSM6GuJ; slave_bizuin=3896466306; data_bizuin=3896466306; bizuin=3896466306; data_ticket=mZvFzflfbgud+SQaD+LO/dgc1odn6PLfAshZ/cCIyoUTjEh6rOMe5rrm8ZqDr2hs; slave_sid=TXlOY1puWng4WmFhOWo2Y1cyQXZqZ0hCbm56dG1ERXRTNm5tSW84cFRtNXJFYVRTZnZWU1NNOW00c3ZJSlBkVVlHazJRWXdjZzJtemZ5dVhKbzFuNjY5cVRiQVhMNl9RR3FIRnpiaHBUOEhiM2I4VlVySDl1eHhKcXlzckRmNTE5SkN4VVdMQVB0TGF3ZHRP; slave_user=gh_d604d5e48425; xid=dcf0aac7445d1669bd61707a4999966b; rewardsn=; wxtokenkey=777'

    # python爬虫与数据挖掘的cookie
    # official_cookie = 'appmsglist_action_3896466306=card; ua_id=Plf3lhpcGuv9m4K6AAAAADOfgjClZ-Mz3LSTjE4JKi4=; pgv_pvi=1331574784; openid2ticket_oLuIc5MVg0Zulj1z7pjK4Mq0vRJs=; mm_lang=zh_CN; pgv_pvid=172926700; openid2ticket_oTQ_25YIAYrrlcCyvLO7mRvoPqg8=; openid2ticket_ogls_6Jj6NFF48wSygfQL-wIrAs4=; wxuin=99791591857567; pgv_si=s2552370176; uuid=8809b5f014c06aa8f3f56915aebed01e; rand_info=CAESIJ81QMFo5rZWaGNf3NkMrYZMvUC73jG6jJX2oVSM6GuJ; slave_bizuin=3896466306; data_bizuin=3896466306; bizuin=3896466306; data_ticket=mZvFzflfbgud+SQaD+LO/dgc1odn6PLfAshZ/cCIyoUTjEh6rOMe5rrm8ZqDr2hs; slave_sid=TXlOY1puWng4WmFhOWo2Y1cyQXZqZ0hCbm56dG1ERXRTNm5tSW84cFRtNXJFYVRTZnZWU1NNOW00c3ZJSlBkVVlHazJRWXdjZzJtemZ5dVhKbzFuNjY5cVRiQVhMNl9RR3FIRnpiaHBUOEhiM2I4VlVySDl1eHhKcXlzckRmNTE5SkN4VVdMQVB0TGF3ZHRP; slave_user=gh_d604d5e48427; xid=dcf0aac7445d1669bd61707a4999966b; rewardsn=; wxtokenkey=777'

    # 微信客户端打开对应公众号的某篇文章，使用fiddler抓包，获取appmsg_token和wechat_cookie
    appmsg_token = '1078_aiOBnjPMEwQ7dXtFs_55-z2hMnwmuuyNQeHUbkfG5kAhOURv7tMOfu3RTetlEXH-hHxKyXDmAFDUSsa8'
    wechat_cookie = 'rewardsn=; wxtokenkey=777; wxuin=748536319; devicetype=Windows10x64; version=62090529; lang=zh_CN; pass_ticket=MzsE4E9UUNjPBN69oq3295yEK3YNYSBOFKlqPF2gdKjqKRAPpaTgqWMyRmSsf3BY; wap_sid2=CP+D9+QCEooBeV9ITGNjdEJsM0N1NTFDb3VNd2ZTSVN0MkFZYm12eHVrdWRFd25rOEdPakFDNGRpUVhMREdqVUJYYnltalhBcDFkR25UazI4emN3LURYcnJyYnU0aDgtWl9FdF9CYWRKbmt3dHRtTTJlMV8yNnFaVzNGbFUxR0hqcEdDVzNGRlZHUVpCUVNBQUF+MIyB9PoFOA1AAQ=='
    official_account = OfficialAccount(nickname=nickname, fakeid=fakeid, official_token=official_token,
                                       official_cookie=official_cookie,
                                       appmsg_token=appmsg_token, wechat_cookie=wechat_cookie, begin_page=121)
    official_account.logger.info('*' * 30 + '开始运行公众号爬虫' + '*' * 30)
    official_account.run()
    official_account.logger.info('*' * 30 + '公众号爬虫运行结束，停止所有爬取工作' + '*' * 30)
