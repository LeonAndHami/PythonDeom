# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class QsSpider(CrawlSpider):
    name = 'qs'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']

    rules = (
        Rule(LinkExtractor(allow=r'https://www.qiushibaike.com/text/page/\d{1,2}/'), callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        divs = response.xpath('//div[@id="content-left"]/div')
        for div in divs:
            item = {}
            item['author'] = div.xpath(".//h2/text()").extract_first().replace("\n", "")
            item['gender'] = "female" if "womenIcon" in div.extract() else "male"
            item['content'] = [x.replace("\n", "").replace("\u3000", "") for x in
                               div.xpath(".//div[@class='content']//span/text()").extract()]
            if item['content'][-1] == "查看全文":
                url = "https://www.qiushibaike.com" + div.xpath(
                    ".//a[@class='contentHerf']/@href").extract_first()
                yield scrapy.Request(url, callback=self.get_detail, meta=item)
            yield item


    def get_detail(self, response):

        pass
