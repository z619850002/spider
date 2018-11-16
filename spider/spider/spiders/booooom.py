import scrapy
import json
import datetime
import sys
from termcolor import *


sys.path.append('../')
from database import model


class DesignModoSpider(scrapy.Spider):
    name = "boom"

    def start_requests(self):
        urls = [
            'https://www.booooooom.com/blog/design/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):
        articles = response.css("article[class='grid-item']")
        print(colored(len(articles), "red"))

        for li in articles:
            title = li.css("h2[class = 'sub-item__title h3'] ::text").extract()[0]
            url = li.css("a[class='grid-item__link'] ::attr(href)").extract()[0]
            #Date can be parsed by the url.
            url_list = url.split('/')
            date = datetime.date(year = int(url_list[-5]) , month=int(url_list[-4]) , day=int(url_list[-3]))
            print(colored(date , "red"))
            timedelta = datetime.timedelta(days=3)
            if datetime.datetime.strptime(str(date), '%Y-%m-%d') < datetime.datetime.today() - timedelta:
                return
            element = model.Element(title=title , url=url , date=date)
            element.save()
        nextURL = response.css("a[class='next page-numbers']::attr(href)").extract()
        if (nextURL):
            yield scrapy.Request(url=nextURL[0], callback=self.parse)
