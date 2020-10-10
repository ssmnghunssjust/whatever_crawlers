# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     dazhongdianping_anti_font.py 
   Description :   None
   Author :        LSQ
   date：          2020/9/1
-------------------------------------------------
   Change Activity:
                   2020/9/1: None
-------------------------------------------------
"""
import requests
import time
import re
import json
from fontTools.ttLib import TTFont
from urllib.request import urlretrieve
import hashlib


# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
#     'Cookie': '_lxsdk_cuid=17401dac830c8-077c5ad72a7ba-4353760-1fa400-17401dac830c8; _lxsdk=17401dac830c8-077c5ad72a7ba-4353760-1fa400-17401dac830c8; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1599040865; _hc.v=c11f553d-7b0e-76ef-6e30-fc210337f543.1599040865; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1599049329; _lxsdk_s=1744eec230d-31f-da7-e1%7C%7C1',
#     'Host': 'www.dianping.com',
# }
#
# resp = requests.get('http://www.dianping.com/shop/14741057', headers=headers)
# # with open('resp.html', 'w', encoding='utf-8') as f:
# #     f.write(resp.content.decode())
# css_url = 'https://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/9fd967fdbc4dc45a848f58190d58ca09.css'
# css_resp = requests.get(css_url)
# font_url_list = re.findall(
#     r'@font-face{font-family: "PingFangSC-Regular-(.*?)";src:url\(.*?\);src:url\(".*?"\) format\("embedded-opentype"\),url\("(.*?)"\);}',
#     css_resp.content.decode(), re.DOTALL)
# start = time.time()
# font_url_set = set()
# font_url_dict = dict()
# font_dict = dict()
# for font_class, font_url in font_url_list:
#     if font_url not in font_url_set:
#         font_url_set.add(font_url)
#         font_file = urlretrieve('https:' + font_url, font_class + '.woff')
#         ttfont = TTFont(font_file[0])
#         # ttfont.saveXML(font_class+'.xml')
#         glyphs = ttfont['glyf']
#         font_url_dict[font_url] = glyphs
#         font_dict[font_class] = glyphs
#     else:
#         font_dict[font_class] = font_url_dict.get(font_url)
# del font_url_dict
#
# # hours_ttfont = TTFont('address.woff')
# # cmap = hours_ttfont.getBestCmap()
# # del cmap[120]
# hours_glyphs = font_dict['hours']
# shopdesc_glyphs = font_dict['shopdesc']
# review_glyphs = font_dict['review']
# num_glyphs = font_dict['num']
# dishname_glyphs = font_dict['dishname']
# address_glyphs = font_dict['address']
# # glyphs_order = hours_ttfont.getGlyphOrder()
# # glyphs_order.remove('glyph00000')
# # glyphs_order.remove('x')
# # font_map = dict()
# font = '1234567890店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺花专东肉菜学福饭人百餐茶务通味所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西批坊州牛佳化五米修爱北养卖建材三会鸡室红站德王光名丽油院堂烧江社合星货型村自科快便日民营和活童明器烟育宾精屋经居庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加麻联卫川泰色世方寓风幼羊烫来高厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺内侧元购前幢滨处向座下累凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团外塔杨铁浦字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位能较境非为欢然他挺着价那意种想出员两推做排实分间甜度起满给热完格荐喝等其再几只现朋候样直而买于般豆量选奶打每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才刚午接重串回晚微周值费性桌拍跟块调糕'
# # for index, name in enumerate(glyphs_order):
# #     glyph = hours_glyphs[name]
# #     coordinates_list = glyph.getCoordinates(hours_glyphs)
# #     digest = hashlib.md5(str(coordinates_list).encode()).hexdigest()
# #     font_map[digest] = font[index]
# # with open('font_map.json', 'w', encoding='utf-8') as f:
# #     f.write(json.dumps(font_map, ensure_ascii=False, indent=4))
# with open('font_map.json', encoding='utf-8') as f:
#     font_map = json.load(f)
# resp_content = resp.content.decode()
# resp_glyphs_code_list = re.findall('<d class="num">(&#x.{4});</d>', resp_content)
# resp_glyphs_name_list = [resp_glyph.replace('&#x', 'uni') for resp_glyph in resp_glyphs_code_list]
# for glyphs_code, glyphs_name in zip(resp_glyphs_code_list, resp_glyphs_name_list):
#     # print(glyphs_code, glyphs_name)
#     coordinates_list = num_glyphs[glyphs_name].getCoordinates(num_glyphs)
#     digest = hashlib.md5(str(coordinates_list).encode()).hexdigest()
#     if font_map.get(digest):
#         result = font_map.get(digest)
#         resp_content = re.sub('<d class="num">' + glyphs_code + ';</d>', result, resp_content)
#
# resp_glyphs_code_list = re.findall('<svgmtsi class="hours">(&#x.{4});</svgmtsi>', resp_content)
# resp_glyphs_name_list = [resp_glyph.replace('&#x', 'uni') for resp_glyph in resp_glyphs_code_list]
# for glyphs_code, glyphs_name in zip(resp_glyphs_code_list, resp_glyphs_name_list):
#     # print(glyphs_code, glyphs_name)
#     coordinates_list = hours_glyphs[glyphs_name].getCoordinates(hours_glyphs)
#     digest = hashlib.md5(str(coordinates_list).encode()).hexdigest()
#     if font_map.get(digest):
#         result = font_map.get(digest)
#         resp_content = re.sub('<svgmtsi class="hours">' + glyphs_code + ';</svgmtsi>', result, resp_content)
#
# resp_glyphs_code_list = re.findall('<e class="address">(&#x.{4});</e>', resp_content)
# resp_glyphs_name_list = [resp_glyph.replace('&#x', 'uni') for resp_glyph in resp_glyphs_code_list]
# for glyphs_code, glyphs_name in zip(resp_glyphs_code_list, resp_glyphs_name_list):
#     # print('address:%s,%s' % (glyphs_code, glyphs_name))
#     coordinates_list = address_glyphs[glyphs_name].getCoordinates(hours_glyphs)
#     digest = hashlib.md5(str(coordinates_list).encode()).hexdigest()
#     if font_map.get(digest):
#         result = font_map.get(digest)
#         resp_content = re.sub('<e class="address">' + glyphs_code + ';</e>', result, resp_content)
#
# resp_glyphs_code_list = re.findall('<svgmtsi class="shopdesc">(&#x.{4});</svgmtsi>', resp_content)
# resp_glyphs_name_list = [resp_glyph.replace('&#x', 'uni') for resp_glyph in resp_glyphs_code_list]
# for glyphs_code, glyphs_name in zip(resp_glyphs_code_list, resp_glyphs_name_list):
#     # print('shopdesc:%s,%s'%(glyphs_code, glyphs_name))
#     coordinates_list = shopdesc_glyphs[glyphs_name].getCoordinates(hours_glyphs)
#     digest = hashlib.md5(str(coordinates_list).encode()).hexdigest()
#     if font_map.get(digest):
#         result = font_map.get(digest)
#         resp_content = re.sub('<svgmtsi class="shopdesc">' + glyphs_code + ';</svgmtsi>', result, resp_content)
#
# resp_glyphs_code_list = re.findall('<svgmtsi class="review">(&#x.{4});</svgmtsi>', resp_content)
# resp_glyphs_name_list = [resp_glyph.replace('&#x', 'uni') for resp_glyph in resp_glyphs_code_list]
# for glyphs_code, glyphs_name in zip(resp_glyphs_code_list, resp_glyphs_name_list):
#     # print('review:%s,%s'%(glyphs_code, glyphs_name))
#     coordinates_list = review_glyphs[glyphs_name].getCoordinates(hours_glyphs)
#     digest = hashlib.md5(str(coordinates_list).encode()).hexdigest()
#     if font_map.get(digest):
#         result = font_map.get(digest)
#         resp_content = re.sub('<svgmtsi class="review">' + glyphs_code + ';</svgmtsi>', result, resp_content)
# print(resp_content)
# with open('resp_new.html', 'w', encoding='utf-8') as f:
#     f.write(resp_content)
#
# end = time.time()
# print('time:%s' % (end - start))


# 1、 发送请求获取响应
# 2、 从响应中提取css的url，再次发送请求，获取css响应
# 3、 从响应中提取font字体文件url，以（font_class，font_url）元组存入font_url_list中
# 4、 遍历font_url_list，
#   4.1、 获取每一个font_class对应的woff文件，
#   4.2、 将woff文件加载为ttfont对象，并得到ttfont对象中的所有glyf字形数据，
#   4.3、 以font_class：glyphs保存到字典中
#   4.4、 重复的font_url不再重新获取woff文件，
# 5、 根据目标提取数据的class属性来确定即将用到的glyphs对象，如class="num"，就从font_dict['num']获得所有glyphs字形数据
# {md5: 数字或汉字}}

class DaZhongDianPing(object):
    def __init__(self, url, cookie, font_map='font_map.json', ):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Cookie': cookie,
            'Host': 'www.dianping.com',
        }
        with open(font_map, encoding='utf-8') as f:
            self.font_map = json.load(f)

    def get_response_decode(self):
        return requests.get(self.url, headers=self.headers).content.decode()

    def get_font_dict(self, response, download=False):
        css_url = re.findall(r'</script>.*?<link rel="stylesheet" type="text/css" href="(//s3plus.*?/svgtextcss/.*?)">', response, re.DOTALL)
        print(css_url)
        css_url = 'http:' + css_url[0]
        css_resp_decode = requests.get(css_url).content.decode()
        # print(css_resp_decode)
        font_url_list = re.findall(
            r'@font-face.*?{font-family: "PingFangSC-Regular-(.*?)";src:url\(.*?\);src:url\(".*?"\) format\("embedded-opentype"\),url\("(.*?)"\);}',
            css_resp_decode, re.DOTALL)
        print(font_url_list)
        font_url_set = set()
        font_url_dict = dict()
        font_dict = dict()
        if download:
            for font_class, font_url in font_url_list:
                if font_url not in font_url_set:
                    font_url_set.add(font_url)
                    font_file = urlretrieve('http:' + font_url, font_class + '.woff')
                    ttfont = TTFont(font_file[0])
                    glyphs = ttfont['glyf']
                    font_url_dict[font_url] = glyphs
                    font_dict[font_class] = glyphs
                else:
                    font_dict[font_class] = font_url_dict.get(font_url)
            del font_url_dict
            return font_dict
        else:
            for font_class, font_url in font_url_list:
                if font_url not in font_url_set:
                    font_url_set.add(font_url)
                    ttfont = TTFont(font_class + '.woff')
                    glyphs = ttfont['glyf']
                    font_url_dict[font_url] = glyphs
                    font_dict[font_class] = glyphs
                else:
                    font_dict[font_class] = font_url_dict.get(font_url)
            del font_url_dict
            return font_dict

    def character_replace(self, resp_content, font_dict):
        for font_class in font_dict.keys():
            glyphs = ''
            expression1 = ''
            expression2 = ''
            if font_class == 'num':
                glyphs = font_dict['num']
                expression1 = '<d class="num">(&#x.{4});</d>'
                expression2 = '<d class="num">{};</d>'
            elif font_class == 'hours':
                glyphs = font_dict['hours']
                expression1 = '<svgmtsi class="hours">(&#x.{4});</svgmtsi>'
                expression2 = '<svgmtsi class="hours">{};</svgmtsi>'
            elif font_class == 'address':
                glyphs = font_dict['address']
                expression1 = '<e class="address">(&#x.{4});</e>'
                expression2 = '<e class="address">{};</e>'
            elif font_class == 'shopdesc':
                glyphs = font_dict['shopdesc']
                expression1 = '<svgmtsi class="shopdesc">(&#x.{4});</svgmtsi>'
                expression2 = '<svgmtsi class="shopdesc">{};</svgmtsi>'
            elif font_class == 'review':
                glyphs = font_dict['review']
                expression1 = '<svgmtsi class="review">(&#x.{4});</svgmtsi>'
                expression2 = '<svgmtsi class="review">{};</svgmtsi>'
            elif font_class == 'dishname':
                glyphs = font_dict['dishname']
                expression1 = '<svgmtsi class="dishname">(&#x.{4});</svgmtsi>'
                expression2 = '<svgmtsi class="dishname">{};</svgmtsi>'
            resp_glyphs_code_list = re.findall(expression1, resp_content)
            resp_glyphs_name_list = [resp_glyph.replace('&#x', 'uni') for resp_glyph in resp_glyphs_code_list]
            for glyphs_code, glyphs_name in zip(resp_glyphs_code_list, resp_glyphs_name_list):
                coordinates_list = glyphs[glyphs_name].getCoordinates(glyphs)
                digest = hashlib.md5(str(coordinates_list).encode()).hexdigest()
                if self.font_map.get(digest):
                    result = self.font_map.get(digest)
                    resp_content = re.sub(expression2.format(glyphs_code), result, resp_content)
        return resp_content


if __name__ == '__main__':
    start = time.time()
    url = 'http://www.dianping.com/shop/l6T0EfR37WXJLarR'
    cookie = '_lxsdk_s=1744fa8e763-8ee-186-cbe%7C%7C1'
    dazhongdianping = DaZhongDianPing(url, cookie)
    response = dazhongdianping.get_response_decode()
    font_dict = dazhongdianping.get_font_dict(response, download=True)
    response = dazhongdianping.character_replace(response, font_dict)
    with open('dazhogndianping_new.html', 'w', encoding='utf-8') as f:
        f.write(response)
    end = time.time()
    print('time:%s' % (end - start))
