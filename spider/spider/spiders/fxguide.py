import scrapy
import json
import datetime
import sys

sys.path.append('../')
from database import model
import json
from termcolor import *


class MicrosoftSpider(scrapy.Spider):
    name = "fxguide"

    def start_requests(self):
        urls = [
            'https://www.fxguide.com/articles/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):
        articles = response.css('article')
        for item in articles:
            date_info = item.css('time ::attr(datetime)').extract()[0]
            date = datetime.datetime.strptime(date_info, '%Y-%m-%d')
            date = datetime.date(date.year , date.month , date.day)
            title_dom = item.css('header h2 a')
            title = title_dom.css('::text').extract()[0]
            url = title_dom.css('::attr(href)').extract()[0]
            element = model.Element(title=title , date=date , url=url)
            element.save()
            print(colored(date , 'red'))








