# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exporters import JsonItemExporter
from jinshi.items import riliItem,InfoItem


class JinshiPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonPipeline(object):
    # def __init__(self):
    #     self.file = open('rili.txt','w')
    # print('JsonPipeline')
    def open_spider(self,spider):
        # with open('rili.json','w+',encoding='utf8') as self.file:
        # self.file = open('rili.json','w+',encoding='utf8')
        self.file = open('rili.txt','w',encoding='utf-8')
        # print('file hand =',self.file)
        # pass

    def process_item(self,item,spider):
        # pass
        if isinstance(item,riliItem):
            lines = json.dumps(dict(item),ensure_ascii=False) + '\n'
            # l = str(item['title']) + '\n'
            # self.file.write(item)
            # self.file.write(l)
            self.file.write(lines)
            # self.file.write('test')
            # print('l =',l)
            # print('lines =',lines)
        return item

    def close_spider(self,spider):
        self.file.close()

class JsonInfoPipeline(object):
    def open_spider(self,spider):
        self.file = open('Info.txt','w',encoding='utf-8')
        # pass

    def process_item(self,item,spider):
        if isinstance(item,InfoItem):
            # print('pipeline item = ',item)
            lines = json.dumps(dict(item),ensure_ascii=False) + '\n'
            self.file.write(lines)
        return item

    def close_spider(self,spider):
        self.file.close()
        # pass

class JsonExPipeline(object):
    # def open_spider(self,spider):
    def open_spider(self, spider):
        # 可选实现，当spider被开启时，这个方法被调用。
        # 输出到tongcheng_pipeline.json文件
        self.file = open('exprotrili.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spier(self, spider):
        # 可选实现，当spider被关闭时，这个方法被调用
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
