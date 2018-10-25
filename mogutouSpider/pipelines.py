# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.conf import settings
import os
import scrapy


# 继承 scrapy.pipelines.imagesImagesPipeline
class MogutouspiderPipeline(ImagesPipeline):

    # 读取配置文件IMAGES_STORE
    IMAGES_STORE = settings.get("IMAGES_STORE")

    # 重写方法
    def get_media_requests(self, item, info):
        if item['img_url']:
            image_url = item['img_url']
            yield scrapy.Request(image_url)

    # 重写方法
    def item_completed(self, results, item, info):
        # 获取图片保存路径
        image_path = [x['path'] for ok,x in results if ok]
        # 图片保存路径 自动保存在setting.py 中的IMAGES_STORE 的路径

        # 自定义保存目录
        if not os.path.exists(self.IMAGES_STORE + "/full/" + item['folder']):
            # 创建目录
            os.mkdir(self.IMAGES_STORE + "/full/" + item['folder'])
        # 移动已经保存好的图片
        print("保存"+self.IMAGES_STORE + "/full/" + item['folder'] + "/" + item['img_url'][-14:])
        os.rename(self.IMAGES_STORE + "/" + image_path[0], self.IMAGES_STORE + "/full/" + item['folder'] + "/" + item['img_url'][-14:])







