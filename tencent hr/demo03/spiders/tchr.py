# -*- coding: utf-8 -*-
import scrapy
import json
import math
from demo03.items import TencentItem
from demo03 import settings

class TchrSpider(scrapy.Spider):
    name = 'tchr'
    allowed_domains = ['tencent.com']
    page_index = 1
    temp_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?pageIndex={}&pageSize=100&language=zh-cn&area=cn'
    start_urls = [temp_url.format(1)]

    def parse(self, response):
        datas = json.loads(response.text)
        for job in datas["Data"]["Posts"]:
            item = TencentItem()
            for field in item.fields:
                item[field] = job[field]
            yield item
        else:
            self.page_index += 1
            if self.page_index <= math.ceil(datas["Data"]["Count"] / 100):
                yield scrapy.Request(self.temp_url.format(self.page_index), callback=self.parse)
