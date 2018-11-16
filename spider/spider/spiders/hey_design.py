import scrapy
import datetime
import sys
sys.path.append('../')
from database import model
from termcolor import *


target = 'https://heydesign.com/page/'
page_num = 1


class heydesign(scrapy.Spider):
    name = "heydesign"

    def start_requests(self):
        urls = [
            'https://heydesign.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        global page_num
        page_num += 1
        for item in response.css('article'):
            if len(item.css('::attr(id)').extract()) > 0:
                href = item.css('h2 a').css('::attr(href)').extract()[0]
                title = item.css('h2 a').css('::text').extract()[0]
                date = item.css('.cb-date').css('time').css('::attr(datetime)').extract()[0]
                # if datetime.datetime.strptime(date, '%Y-%m-%d') < datetime.datetime.today():
                #     return
                print(colored(date , "red"))
                date = datetime.datetime.strptime(date, '%Y-%m-%d')
                timedelta = datetime.timedelta(days=3)
                if date < datetime.datetime.today() - timedelta:
                    return
                element = model.Element(title=title, date=date, url=href)
                element.save()
        if page_num <= 32:
            next_url = target + str(page_num) + '/'
            yield scrapy.Request(url=next_url, callback=self.parse)