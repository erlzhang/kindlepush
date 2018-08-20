# -*- coding: utf-8 -*-
import scrapy
import json
import datetime

from kindle.items import KindleItem
from scrapy.selector import Selector

class CkxxSpider(scrapy.Spider):
    name = 'ckxx'
    allowed_domains = ['cankaoxiaoxi.com']
    start_urls = ['http://app.cankaoxiaoxi.com/?app=shlist&controller=milzuixin&action=world&page=1&pagesize=20']

    def parse(self, response):
        date = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
        body = response.body[1:-1]
        body = json.loads(body)
        data = body["data"]
        links = Selector(text=data).xpath("//a/@href").extract()

        for link in links:
            if date not in link:
                return
            yield scrapy.Request(link, self.parse_article, dont_filter=False)

    def parse_article(self, response):
        item = KindleItem()
        item['resource'] = "参考消息国际版"
        item['title'] = response.xpath("//h1[contains(@class, 'YH')]/text()").extract_first()
        item['content'] = response.xpath('//div[contains(@class, "article-content")]').extract_first()
        item['url'] = response.url

        if '延伸阅读' in item['content'] :
            return

        next_link = response.xpath("//p[contains(@class, 'fz-16')]/strong/a/@href").extract_first()

        if( next_link ):
            yield scrapy.Request(next_link, self.parse_article, dont_filter=False)

        yield item
