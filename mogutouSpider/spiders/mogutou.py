# -*- coding: utf-8 -*-
import scrapy
from mogutouSpider.items import MogutouspiderItem

class MogutouSpider(scrapy.Spider):
    name = 'mogutou'
    allowed_domains = ['wxcha.com']
    start = input("从哪一页开始：")
    stop = input("到哪一页")

    # 不输入默认第一页
    if not start:
        start = 1
    if not stop:
        stop = start

    url = 'http://www.wxcha.com/biaoqing/t/mogutou/update_'
    start_urls = [
        url + str(start) + ".html"
    ]

    def parse(self, response):

        """
        :param response:
        :return:
        """
        for each in response.xpath("//ul[@class='newtx_ul cl']/li/a/@href"):
            # 内容页url地址
            content_url = each.extract()
            # 解析内容页
            yield scrapy.Request(content_url, callback=self.parse_content)

        if int(self.start) < int(self.stop):
            self.start = int(self.start)
            self.start += 1
            # 继续爬下一页
            yield scrapy.Request(self.url + str(self.start) + ".html", callback=self.parse)

    def parse_content(self, response):
        """
        解析内容页
        :param response:
        :return:
        """
        for each in response.xpath("//ul[contains(@class, 'tupian3_ul')]/li"):

            item = MogutouspiderItem()
            # 图片url
            item['img_url'] = each.xpath("./img/@data-original").extract()[0]
            # 保存图片的目录
            item['folder'] = each.xpath("./img/@alt").extract()[0]
            # 图片交给ImagePipelines处理
            yield item





