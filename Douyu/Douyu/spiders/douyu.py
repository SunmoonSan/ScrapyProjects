# -*- coding: utf-8 -*-
import scrapy
import json

from Douyu.items import DouyuItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    # allowed_domains = ['douyu.cn']
    # http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset=10
    base_url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='
    offset = 0
    start_urls = ['http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset=0']

    def parse(self, response):
        datas = json.loads(response.body)['data']
        if len(datas) == 0:
            return
        
        for data in datas:
            item = DouyuItem()
            item['nickname'] = data['nickname']
            item['image_link'] = data['vertical_src']

            yield item

        self.offset += 20
        yield scrapy.Request(self.base_url + str(self.offset), callback=self.parse)
