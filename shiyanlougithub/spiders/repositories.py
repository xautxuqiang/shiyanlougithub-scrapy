# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import RepositoriesItem

class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1,5))

    def parse(self, response):
        for repositority in response.css('li.source'):
            item = RepositoriesItem({
                'name': repositority.css('div.mb-1 h3 a::text').re_first('[\s]*(\S*)'),
                'update_time': repositority.css('div.mt-2 relative-time::attr(datetime)').extract_first()
            })
            yield item

