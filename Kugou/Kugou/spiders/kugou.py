# -*- coding: utf-8 -*-
import scrapy
from Kugou.items import KugouItem


class KugouSpider(scrapy.Spider):
    name = 'kugou'
    allowed_domains = ['www.kugou.com']
    start_urls = ['http://www.kugou.com/yy/rank/home/1-8888.html?from=rank']

    # n = 1

    def parse(self, response):
        lis = response.xpath("//li[@class=' ']")
        for li in lis:

            singer_song = li.xpath("@title").extract_first().split('-')
            singer = singer_song[0].strip()
            song = singer_song[1].strip()            
            index = li.xpath("./span[@class='pc_temp_num']//text()").extract_first().strip()
            print('>>>>index>>>', index)
            time = li.xpath("./span/span[@class='pc_temp_time']/text()").extract_first().strip()         
            url = li.xpath("./a/@href").extract_first().strip()
            item = KugouItem(singer=singer, song=song, time=time, index=index)
            
            request = scrapy.Request(url=url, callback=self.parse_lyric)                    
            request.meta['item'] = item
            yield request

        for n in range(2, 23):
            next_url = 'http://www.kugou.com/yy/rank/home/' + str(n) + '-8888.html?from=rank'
            print('>>>>>>', next_url)
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_lyric(self, response):
        # self.n = self.n + 1
        itme = response.meta['item']
        lyric = response.xpath("//div[@class='displayNone']/text()").extract_first()
        itme["lyric"] = lyric
        
        yield itme

