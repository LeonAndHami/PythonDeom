import requests
from scrapy.selector import Selector
import json


class QiuShiSpider(object):

    def __init__(self):
        self.start_url = "https://www.qiushibaike.com/text/page/{}/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}

    def parse_url(self, url):
        html = requests.get(url, headers=self.headers)
        return html

    def get_content_list(self, response):
        selector = Selector(response)
        divs = selector.xpath("//div[@id='content-left']/div")

        content_list = []
        for div in divs:
            item = {}
            if "匿名用户" in div.extract():
                item["author"] = None
                item["gender"] = "匿名用户"
                item["age"] = None
            else:
                item["author"] = div.xpath(".//h2/text()").extract_first().replace("\n", "")
                item["gender"] = "man" if "manIcon" in div.xpath(
                    ".//div[contains(@class,'Icon')]/@class").extract_first() else "woman"
                item["age"] = div.xpath(".//div[contains(@class,'Icon')]/text()").extract_first()

            url = "https://www.qiushibaike.com" + div.xpath(".//a[@class='contentHerf']/@href").extract_first()
            temp_content = div.xpath(".//div[@class='content']//span/text()").extract()
            if '查看全文' in temp_content:
                temp_content = requests.get(url, headers=self.headers)
                item["content"] = Selector(temp_content).xpath("//div[@class='content']/text()").extract()
            else:
                item["content"] = temp_content
            item["content"] = [i.replace("\n", "") for i in item["content"]]
            content_list.append(item)
        return content_list

    def save_to_file(self, content_list):
        with open("d:/qiushi.txt", "a", encoding="utf-8") as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n\n")

    def run(self):
        for i in range(1, 13):
            url = self.start_url.format(i)
            html = self.parse_url(url)
            content_list = self.get_content_list(html)
            self.save_to_file(content_list)
            print(url)


if __name__ == "__main__":
    spider = QiuShiSpider()
    spider.run()
