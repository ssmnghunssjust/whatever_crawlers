import requests

class TiebaCrawler:
    def __init__(self, kw, max_page):
        '''
        :param kw: 贴吧名称
        :param max_page: 爬取最大页数
        '''
        self.tieba_name = kw
        self.max_page = max_page
        self.base_url = 'https://tieba.baidu.com/f?kw='+ kw +'&pn={}'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        return response

    def get_content(self, response):
        return response.content.decode()

    def save_html(self, content, page):
        html_name = self.tieba_name + '吧_' + str(page) + '.html'
        with open(html_name, 'w', encoding='utf-8') as f:
            f.write(content)

    def run(self):
        page_num = 0
        page = 1
        for i in range(self.max_page):
            # 1、构造首页url
            url = self.base_url.format(page_num)
            print(url)
            # 2、发起请求、获取响应
            response = self.parse_url(url)
            # 3、提取数据
            content = self.get_content(response)
            # 4、保存数据
            self.save_html(content, page)
            print('第{}页保存成功！'.format(page))
            # 5、构造下一页url，重复步骤2-5
            page_num += 50
            page += 1


if __name__ == '__main__':
    tieba_crawler = TiebaCrawler('洛奇英雄传', max_page=10)
    tieba_crawler.run()