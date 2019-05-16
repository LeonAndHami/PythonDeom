import requests
import os


class TiebaSpider(object):

    def __init__(self, spider_name):
        self.spider_name = spider_name
        self.base_url = "https://tieba.baidu.com/f?kw=" + spider_name + "&ie=utf-8&pn={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}
        self.save_path = os.path.join(os.curdir, "html")

    def get_url_list(self):
        return [self.base_url.format(i * 50) for i in range(1000)]

    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def save_html(self, html, page_index):
        file_name = "{} 第 {} 页.html".format(self.spider_name, page_index + 1)
        file_name = os.path.join(self.save_path, file_name)
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(html)

    def run(self):
        urls = self.get_url_list()
        for url in urls:
            html = self.parse_url(url)
            self.save_html(html, urls.index(url))


if __name__ == "__main__":
    spider = TiebaSpider("DNF")
    spider.run()
