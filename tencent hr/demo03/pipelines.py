# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

# 本地mongodb默认端口，实例客户端，可以不写host和port
context = MongoClient()["tencent"]["hr"]


class TencnetPipeline(object):
    def process_item(self, item, spider):
        # 记得转字典！！！
        print(item)
        # context.insert_one(dict(item))
        return item
