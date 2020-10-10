# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     anti_font.py 
   Description :   None
   Author :        LSQ
   date：          2020/8/20
-------------------------------------------------
   Change Activity:
                   2020/8/20: None
-------------------------------------------------
"""
from gevent import monkey, pool

monkey.patch_all()
import gevent
import requests
import time
import re
import os
import pytesseract
import matplotlib.pyplot as plt

from urllib.request import urlretrieve
from fontTools.ttLib import TTFont
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed


class MaoyanCrawler(object):

    def __init__(self, url):
        # 创建协程池
        self.pool = pool.Pool()

        # 创建线程池
        # self.pool = ThreadPoolExecutor()
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Referer': 'https://maoyan.com/',
            'Cookie': 'uuid_n_v=v1; uuid=E510ABB0E2E311EA94345B95E7867004EFAB84BDD3994C418FA4F2CF9D361735; _lxsdk_cuid=173af6c9db0c8-08411902659abe-4353760-1fa400-173af6c9db1c8; _lxsdk=E510ABB0E2E311EA94345B95E7867004EFAB84BDD3994C418FA4F2CF9D361735; mojo-uuid=3debffd1a8d5c231ec8beb1c1aa2a76d; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1597927901,1598277496,1598494449,1598602553; mojo-session-id={"id":"2a84ecfd142e70fc77039930309c2638","time":1598672909698}; _csrf=5b7732b9ca8daca9c720525e928857cd2999743ec3eeb4178d719f4ca6443cb9; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1598674310; mojo-trace-id=7; __mta=150715273.1597927901843.1598672987933.1598674310352.28; _lxsdk_s=1743854b5fd-00d-849-08f%7C%7C14'
        }

    def file_delete(self, file_name):
        if os.path.exists(file_name):
            os.remove(file_name)

    def get_response_decode(self):
        maoyan_resp = requests.get(self.url, headers=self.headers)
        maoyan_text = maoyan_resp.content.decode()
        return maoyan_text

    def get_woff(self, response_decode):
        woff_url = re.findall("url\('(.*?)'\) format\('woff'\);", response_decode)
        if woff_url:
            woff_url = 'https:' + woff_url.pop()
        woff_file = urlretrieve(woff_url, 'maoyan.woff')
        return woff_file[0]

    def extract_all_characters(self, woff_file):
        ttfont = TTFont(woff_file)
        glyph_names = ttfont.getGlyphNames()
        glyphs = ttfont['glyf']
        font_map = dict()
        # 提取字符

        # 协程池
        # glyph_names.remove('glyph00000')
        # glyph_names.remove('x')
        # coroutine_list = [self.pool.spawn(self.extract_single_character, glyph_name, glyphs) for glyph_name in
        #                   glyph_names]
        # gevent.joinall(coroutine_list)
        # for coroutine in coroutine_list:
        #     font_map.update(coroutine.value)
        # del coroutine_list

        # 线程池
        glyph_names.remove('glyph00000')
        glyph_names.remove('x')
        thread_list = []
        with ThreadPoolExecutor() as pool:
            for glyph_name in glyph_names:
                thread = pool.submit(self.extract_single_character, glyph_name, glyphs)
                thread_list.append(thread)
            for future in as_completed(thread_list):
                font_map.update(future.result())
        return font_map

    def extract_single_character(self, glyph_name, glyphs):
        list_a = list()
        list_b = list()
        coordinates_list = glyphs[glyph_name].getCoordinates(glyphs)[0]
        for index, coordinate in enumerate(coordinates_list[:-1], start=1):
            if 160 < abs(coordinates_list[index][0] - coordinate[0]) and 160 < abs(
                    coordinates_list[index][1] - coordinate[1]):
                list_a = coordinates_list[:index]
                list_b = coordinates_list[index:]
                break
        plt.draw()
        plt.figure(figsize=(0.4, 0.6))
        if list_a and list_b and (len(list_a) + len(list_b) > 20):
            list_a_x = list()
            list_a_y = list()
            list_b_x = list()
            list_b_y = list()
            for x, y in list_a:
                list_a_x.append(x)
                list_a_y.append(y)
            for x, y in list_b:
                list_b_x.append(x)
                list_b_y.append(y)
            plt.fill(list_a_x, list_a_y, 'black', list_b_x, list_b_y, 'white')
        else:
            y_list = list()
            x_list = list()
            for x, y in coordinates_list:
                x_list.append(x)
                y_list.append(y)
            plt.fill(x_list, y_list, "black")
        # plt.fill(x_list, y_list, facecolor="black", edgecolor='none', alpha=0.5, linewidth=3)
        plt.axis('off')
        bio = BytesIO()
        plt.savefig(bio)
        # plt.show()
        im = Image.open(bio)
        glyph_name = glyph_name.replace('uni', '&#x').lower() + ';'
        return {glyph_name: pytesseract.image_to_string(im, config='--psm 6')[0]}

    def replace(self, font_map, response_decode):
        for name, value in font_map.items():
            response_decode = response_decode.replace(name, value)
        return response_decode


if __name__ == '__main__':
    start = time.time()
    # 初始化猫眼爬虫
    crawler = MaoyanCrawler(url='https://maoyan.com/cinemas')
    # 删除已存在的字体文件
    crawler.file_delete('maoyan.woff')
    # 获取响应
    response_decode = crawler.get_response_decode()
    # 获取woff字体文件
    woff_file = crawler.get_woff(response_decode)
    # 提取字体文件的字符
    font_map = crawler.extract_all_characters(woff_file)
    print('font_map:%s' % font_map)
    # 根据font_map将response_decode中的不明字符替换为正常数字
    response_decode = crawler.replace(font_map, response_decode)
    # print(response_decode)
    end = time.time()
    print('time: %s' % (end - start))

