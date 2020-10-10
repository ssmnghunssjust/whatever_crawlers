# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     caipanwenshu_mitmproxy.py
   Description :   None
   Author :        LSQ
   date：          2020/9/21
-------------------------------------------------
   Change Activity:
                   2020/9/21: None
-------------------------------------------------
"""
from mitmproxy import ctx
from mitmproxy.http import  HTTPFlow
from redis import StrictRedis

class CaiPanWenShu(object):
    def response(self, flow: HTTPFlow):
        if flow.request.host == 'wenshu.court.gov.cn':
            text = flow.response.get_text()
            text = text.replace('debugger;', '')
            text = text.replace('while(1)', 'while(0)')
            flow.response.set_text(text)

addons = [CaiPanWenShu()]