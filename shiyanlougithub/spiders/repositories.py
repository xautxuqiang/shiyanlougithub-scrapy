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
        for repositority in response.css('li.col-12'):
            item = RepositoriesItem()
            item['name'] = repositority.css('div.mb-1 h3 a::text').re_first('[\s]*(\S*)')
            item['update_time'] = repositority.css('div.mt-2 relative-time::attr(datetime)').extract_first()
            repositority_url = response.urljoin(repositority.css('div.mb-1 h3 a::attr(href)').extract_first())
            request = scrapy.Request(repositority_url, callback=self.parse_number)
            request.meta['item'] = item
            yield request

    def parse_number(self, response):
        item = response.meta['item']
        num_list = []
        for num in response.css('ul.numbers-summary li')[:3]:
            num_list.append(num.css('a span::text').re_first('[^\d]*(\d*)[^\d]*'))
        item['commits'], item['branches'], item['releases'] = num_list
        yield item

