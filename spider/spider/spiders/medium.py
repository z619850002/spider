import scrapy
import sys
sys.path.append('../')
from database import model
import datetime
from termcolor import *


target = 'https://medium.com'


class medium(scrapy.Spider):
    name = "medium"

    def start_requests(self):
        urls = [
            'https://medium.com/topic/design',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        global target
        for item in response.xpath('//div[contains(@class,"en") and contains(@class,"eo") and contains(@class,"d")]').css('section section'):
            url = target + item.css('h3 a').css('::attr(href)').extract()[0]
            title = item.css('h3 a').css('::text').extract()[0]
            request = scrapy.Request(url=url, callback=self.parse2)
            request.meta['title'] = title
            request.meta['url'] = url
            yield request

    def parse2(self, response):
        date = response.css('time').css('::attr(datetime)').extract()[0]
        url = response.meta['url']
        title = response.meta['title']
        date = datetime.datetime.strptime(date[:10], '%Y-%m-%d')
        timedelta = datetime.timedelta(days=3)
        if date < datetime.datetime.today() - timedelta:
            return
        print(colored(date , "red"))
        element = model.Element(title=title, date=date, url=url)
        element.save()
