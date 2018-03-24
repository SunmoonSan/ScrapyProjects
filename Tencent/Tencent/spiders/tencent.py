# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy
from Tencent.items import TencentItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    # allowed_domains = ['tencent.com']
    # https://hr.tencent.com/position.php?start=0#a
    base_url = 'http://hr.tencent.com/position.php?start='
    offset = 10
    start_urls = ['http://hr.tencent.com/position.php?start=0']

    def parse(self, response):
        print(response.body)
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")

        for node in node_list:
            item = TencentItem()
            position_name = node.xpath("./td[1]/a/text()").extract_first()
            position_link = node.xpath("./td[1]/a/@href").extract_first()
            if len(node.xpath("./td[2]/text()")):
                position_type = node.xpath("./td[2]/text()").extract_first()
            else:
                position_type = ""
            position_number = node.xpath("./td[3]/text()").extract_first()
            work_location = node.xpath("./td[4]/text()").extract_first()
            publish_time = node.xpath("./td[5]/text()").extract_first()

            item['position_name'] = position_name
            item['position_link'] = position_link
            item['position_type'] = position_type
            item['position_number'] = position_number
            item['work_location'] = work_location
            item['publish_time'] = publish_time

            yield item

        if not len(response.xpath("//a[@class='noactive' and @id='next']")):
            next_url = response.xpath("//a[@id='next']/@href").extract_first()
            url = 'https://hr.tencent.com/' + next_url
            yield scrapy.Request(url, callback=self.parse) # parse前添加self.
