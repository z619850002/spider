import scrapy
import json
import datetime
import sys

sys.path.append('../')
from database import model
import json
from termcolor import *


class AirbnbSpider(scrapy.Spider):
    name = "airbnb"

    def start_requests(self):
        urls = [
            "https://airbnb.design/articles/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def formatTime(self, raw):
        sp = raw[:10].split('-')
        year = sp[0]
        month = sp[1]
        day = sp[2]
        return datetime.date(int(year), int(month), int(day))

    def parse(self, response):

        articles = response.css('article')

        for item in articles:
            #No date in the website, so I need to use today as the date, the code here need to change in the future.
            date = datetime.date(year=2018 , month=10 , day=1)
            href = item.css('a ::attr(href)').extract()[0]
            title = item.css("a[class = 'h-link'] h2 ::text").extract()[0]
            # This may be useful in the future.
            # subtitle = item.css("a[class = 'h-link'] h3 ::text").extract()[0]

            element = model.Element(title = title , url= href , date = date)
            if element.check_exist() == False:
                element.date = datetime.date.today()
                element.save()
                print(colored(title, 'red'))

