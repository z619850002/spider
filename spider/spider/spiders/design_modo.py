import scrapy
import json
import datetime
import sys

sys.path.append('../')
from database import model


class DesignModoSpider(scrapy.Spider):
    name = "designmodo"

    def start_requests(self):
        urls = [
            'https://designmodo.com/design/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # raw is a string like " • March 24, 2011"
    def formatTime(self, raw):
        sp = raw.split(' ')
        year = sp[4]
        month = sp[2]
        day = sp[3][:-1]
        m = {
            "January": "01",
            "February": "02",
            "March": "03",
            "April": "04",
            "May": "05",
            "June": "06",
            "July": "07",
            "August": "08",
            "September": "09",
            "October": "10",
            "November": "11",
            "December": "12"
        }
        return datetime.date(int(year), int(m[month]), int(day))

    def parse(self, response):
        lis = response.css("ul[class='flex fixedSpaces']").css("li")
        for li in lis:
            href = li.css("a[class='article-element']::attr(href)").extract()
            title = li.css("a[class='article-element']::attr(title)").extract()
            rawTime = li.css("div::text").extract()[0]
            date = self.formatTime(rawTime)
            timedelta = datetime.timedelta(days=3)
            if datetime.datetime.strptime(str(date), '%Y-%m-%d') < datetime.datetime.today() - timedelta:
                return
            element = model.Element(title=title[0], date=date, url=href[0])
            element.save()
        nextURL = response.css("a[class='next page-numbers']::attr(href)").extract()
        if (nextURL):
            yield scrapy.Request(url=nextURL[0], callback=self.parse)
