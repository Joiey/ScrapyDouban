#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string

from douban.items import Subject

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Request, Rule

class MovieSubjectSpider(CrawlSpider):
    name = 'movie_subject'
    allowed_domains = ['m.douban.com']
    start_urls = ['https://m.douban.com/movie/subject/1292052/']
    # 存放定制的获取链接的规则对象（可以是一个列表也可以是元组）
    # 根据规则提取到的所有链接，会由crawlspider构建request对象，并交给引擎处理
    rules = (
        Rule(LinkExtractor(allow=('movie/subject/(\d).*rec$')), # allow=(),设置允许提取的url
             callback='parse_item',
             follow=True,
             process_request='cookie'), #可以设置回调函数，对request对象进行拦截
    )

    def cookie(self, request):
        bid = ''.join(random.choice(string.ascii_letters + string.digits) for
                      x in range(11))
        request.cookies['bid'] = bid
        request = request.replace(url=request.url.replace('?', '/?'))
        return request

    def start_requests(self):
        for url in self.start_urls:
            bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
            yield Request(url, cookies={'bid': bid})

    def get_douban_id(self, subject, response):
        subject['douban_id'] = response.url[35:-10]
        return subject

    def parse_item(self, response):
        subject = Subject()
        self.get_douban_id(subject, response)
        subject['type'] = 'movie'
        return subject
