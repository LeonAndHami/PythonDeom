# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import copy


class QsSpider(CrawlSpider):
    name = 'qs'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']

    rules = (
        # 这里可以加个详情页的规则
        Rule(LinkExtractor(allow=r'https://www.qiushibaike.com/text/page/\d+/'), callback='parse_item',
             follow=True),
    )
    """
    流程：
    1、请求start_urls
    2、rules 规则提取url（提取到的url不一定是第1页）
    3、进入 parse_item方法
    4、parse_item 退出，follow=true，提取下一页url,进行下一轮循环
    
    可以改成从每个帖子的详情页中提取，但这样请求量就增加了。
    """

    def parse_item(self, response):
        print(response.request.url)
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
                yield scrapy.Request(url, callback=self.get_detail, meta=copy.deepcopy(item))
            yield item

    def get_detail(self, response):
        item = response.meta
        item['content'] = [x.replace("\n", "").replace("\u3000", "") for x in
                           response.xpath("//div[@class='content']/text()").extract()]
        # print(item)  # 通过meta传过来之后多几个属性？
        yield item
