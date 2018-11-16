import scrapy
import json
import datetime
import sys
sys.path.append('../')
from database import model

class SpeckyBoySpider(scrapy.Spider):
    name =  "speckyboy"
    def start_requests(self):
        urls = [
            'https://speckyboy.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url , callback=self.parse)

    def formatTime(self, raw):
        sp = raw.split(' ')
        year = sp[-1]
        month = sp[-3]
        day = sp[-2][:-3]
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
        return datetime.date(int(year) , int(m[month]) , int(day))

    def parse(self, response):
        lis = response.css("main[id='main']").css("article")
        for li in lis:
            href = li.css('h2').css('a::attr(href)').extract()
            title = li.css('h2').css('a::attr(title)').extract()
            rawTime = li.css("span[class='meta-date']::text").extract()[0].strip()
            date = self.formatTime(rawTime)
            timedelta = datetime.timedelta(days=3)
            if datetime.datetime.strptime(str(date), '%Y-%m-%d') < datetime.datetime.today() - timedelta:
                return
            # print(href, title, date)
            element = model.Element(title=title[0], date = date, url=href[0])
            element.save()
        nextURL = response.css("a[class='next page-numbers']::attr(href)").extract()
        if(nextURL):
            yield scrapy.Request(url=nextURL[0], callback=self.parse)
