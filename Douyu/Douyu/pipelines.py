# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from settings import IMAGES_STORE as images_store
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class DouyuPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        image_link = item['image_link']
        yield scrapy.Request(image_link)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        os.rename(images_store + image_path[0], images_store + item['nickname'] + '.jpg')

        return item


#   def process_item(self, item, spider):
#       return item
# [(True, {'url': 'https://rpic.douyucdn.cn/live-cover/appCovers/2018/03/12/3008429_20180312102850_big.jpg',
#          'path': 'full/1e54d78407b7d70a19703d3f8eb31d1d5083fa01.jpg', 'checksum': 'eb17a75f6ffdb68b0aed6f05a67207a1'})]
