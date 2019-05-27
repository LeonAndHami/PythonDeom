# -*- coding: utf-8 -*-
import scrapy


class DdSpider(scrapy.Spider):
    name = 'dd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://book.dangdang.com/']

    def parse(self, response):
        divs = response.xpath("//div[@father='1']")[2:12]
        # with open('d:/boo.txt','w',encoding='utf8') as f:
        #     f.write(response.text)
        # 2-- 11

        pass
