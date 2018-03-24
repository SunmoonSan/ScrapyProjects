# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy
from ITcast.items import ItcastItem


class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    # allowed_domains = ['http:www.itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        node_list = response.xpath("//div[@class='li_txt']")
	for node in node_list:
	    item  = ItcastItem()
	    name = node.xpath("./h3/text()").extract_first()
	    title = node.xpath("./h4/text()").extract_first()
	    info = node.xpath("./p/text()").extract_first()
	    print(name, title, info)
	    item['name'] = name
	    item['title'] = title
	    item['info'] = info
	    yield item     
