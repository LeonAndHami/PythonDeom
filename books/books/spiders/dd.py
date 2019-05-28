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
        for div in divs:
            item = {}
            item["level_one"] = [x.strip() for x in div.xpath("./dl/dt//text()").extract() if len(x.strip()) > 0][0]
            dls = div.xpath(".//dl[@class='inner_dl']")
            print(len(dls))
            count = 1
            for dl in dls:
                # with open("d:/temp/dl"+str(count)+".txt","w",encoding="utf8") as f:
                #     f.write(dl.extract())
                item["level_two"] = [x.strip() for x in dl.xpath("./dt/a/text()").extract()]
                if item["level_two"] is None:
                    item["level_two"] = dl.xpath("./dt[position()=1]//text()").extract_first()
                # count += 1
                # a_list = dl.xpath("./dd/a")
                # for a in a_list:
                #     item["level_three"] = a.xpath("./text()").extract_first()
                print(item)
                print("*" * 20)
            # return
            # print(item)
            # print("*" * 20)
        pass
