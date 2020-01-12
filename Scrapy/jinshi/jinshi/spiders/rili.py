# -*- coding: utf-8 -*-
import scrapy
import json
import time
from jinshi.items import riliItem, InfoItem

class RiliSpider(scrapy.Spider):
    name = 'rili'
    allowed_domains = ['jin10.com']
    rilitime = time.strftime("%Y/%m%d",time.localtime())
    # print(rilitime)
    # start_urls = ['https://cdn-rili.jin10.com/data/2020/0102/economics.json']
    start_urls = ['https://cdn-rili.jin10.com/data/'+rilitime+'/economics.json']

    def parse(self, response):
        sites = json.loads(response.body)
        for site in sites:
            # print(site['id'],site['country'],site['country']+site['time_period']+site['name'],site['pub_time'],site['star'])
            riliitem = riliItem()
            riliitem['date'] = site['pub_time']
            riliitem['time'] = site['pub_time']
            riliitem['country'] = site['country']
            riliitem['title'] = site['country']+site['time_period']+site['name']
            riliitem['importantment'] = site['star']
            riliitem['id'] = site['id']
            # print('riliItem =',riliitem)

            yield riliitem
            if riliitem['id']:
                # print('riliItem[id] =',riliitem['id'],' urljoin = ',str(response.urljoin(riliitem['id'])))
                # urljoin() 传入 str 类型 riliItem['id'] 是
                # urljoin() 函数 拼接的是start_urls 连接的主域
                # print('type = ',type(riliitem['id']))
                # infourl = response.urljoin(str(riliitem['id']))
                # print('url = '+str(infourl))

                # 实际需求中 新连接不是 start_urls 中连接主域
                # 需要手动拼接
                info_url = 'https://cdn-rili.jin10.com/data/jiedu/'+str(riliitem['id'])+'.json'
                # print('info_url =',info_url)
                yield scrapy.Request(url=info_url, callback=self.info_parse)
        # yield scrapy.Request(url='https://cdn-rili.jin10.com/data/jiedu/161976.json', callback=self.info_parse)
        # pass
    def info_parse(self,response):
        # json.loads() 将str类型数据转换成dict格式 , response.body 类型是 <'bytes'>
        # 先将response.body 转换成str , 再将 str 转换成 dict
        # infos = json.loads(response.body)
        # print('body type=',type(response.body))
        infos = str(response.body,encoding='utf-8')
        infos = json.loads(infos)
        # print('type=',type(infos))
        # print('info_parse = ',infos)
        # for info in infos:
        # 分析网页发现每个对应的网页只有对应的信息，所以不需要 for
        info_item = InfoItem()
        # print('country = ',infos['country'],' title = ',infos['title'],' impact = ',infos['impact'])
        info_item['country'] = infos['country']
        info_item['title'] = infos['title']
        info_item['impact'] = infos['impact']
        info_item['paraphrase'] = infos['paraphrase']
        # print('info_item =',info_item)
        yield info_item
