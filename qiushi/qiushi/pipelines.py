# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class QiushiPipeline(object):
    def process_item(self, item, spider):
        # print(item)
        # with open("./qiushi.txt", "a", encoding="utf8")as f:
        #     f.write(json.dumps(item, ensure_ascii=False, indent=4))
        #     f.write("\n")
        return item
