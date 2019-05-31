# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
from books.items import BooksItem
from scrapy_redis.spiders import RedisSpider


class DdSpider(RedisSpider):
    name = 'dd'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://book.dangdang.com/']  # 在settngs中加入redis的配置，就可以实现断点续爬、增量式爬虫，但还是单机的。

    # 爬虫类继承，RedisSpider，加上redis_key后，就可以实现分布式爬虫。
    # 只有一台电脑都读取redis_key的url,读取之后，会pop掉，保证别的电脑读不到(不需要start_urls)
    redis_key = "dd"  # 记得往redis_key加入起始url，而且键是list类型  lpush dd http://book.dangdang.com/

    def parse(self, response):
        divs = response.xpath("//div[@father='1']")[2:12]
        for div in divs:
            item = BooksItem()
            item["l_one"] = [x.strip() for x in div.xpath("./dl/dt//text()").extract() if len(x.strip()) > 0][0]
            dls = div.xpath(".//dl[@class='inner_dl']")
            for dl in dls:

                item["l_two"] = [x.strip() for x in dl.xpath("./dt/a/text()").extract()]
                if not item["l_two"]:
                    item["l_two"] = dl.xpath("./dt[position()=1]//text()").extract_first().strip()
                else:
                    item["l_two"] = item["l_two"][0]

                a_list = dl.xpath("./dd/a")
                for a in a_list:
                    item["l_three"] = a.xpath("./text()").extract_first()
                    item['category_url'] = a.xpath("./@href").extract_first()
                    yield scrapy.Request(item['category_url'], callback=self.parse_detail, meta=deepcopy(item))

    def parse_detail(self, response):
        category = response.meta
        li_list = response.xpath("//ul[@id='component_59']/li")
        for li in li_list:
            item = deepcopy(category)
            item["title"] = li.xpath("./a/@title").extract_first()
            item["img"] = li.xpath("./a/img/@src").extract_first()
            if "none" in item['img']:
                item["img"] = li.xpath("./a/img/@data-original").extract_first()
            item["detail"] = li.xpath("./p[@class='detail']/text()").extract_first()
            item["price"] = li.xpath("./p[@class='price']/span/text()").extract_first()
            item['author'] = li.xpath(
                "./p[@class='search_book_author']/span[position()=1]/a/text()").extract_first()
            item['pub_date'] = li.xpath(
                "./p[@class='search_book_author']/span[position()=2]/text()").extract_first().replace(" /", "")
            item['publisher'] = li.xpath(
                "./p[@class='search_book_author']/span[position()=3]/a/text()").extract_first()
            yield item

        next_page = response.xpath("//li[@class='next']/a/@href").extract_first()
        if next_page:
            next_page = "http://category.dangdang.com" + next_page
            yield scrapy.Request(next_page, callback=self.parse_detail, meta=category)
