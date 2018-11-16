import scrapy
import json
import datetime
import sys
sys.path.append('../')
from database import model

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,  datetime.datetime):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)



class QuotesSpider(scrapy.Spider):
    name =  "quotes"
    def start_requests(self):
        urls = [
            'https://designmind.frogdesign.com/2018/',
        ]
        for url in urls:
            yield scrapy.Request(url=url , callback=self.parse)

    def parse(self , response):
        element = response.css('li').css('a')
        for item in element:
            href = item.css('::attr(href)').extract()
            text = item.css('::text').extract()
            #Parse the date.
            dateList = str(href).split('/')
            #Maybe incorrect.
            year = dateList[-4]
            month = dateList[-3]
            day = 1
            date = datetime.date(int(year) , int(month) , day)
            timedelta = datetime.timedelta(days=3)
            if datetime.datetime.strptime(str(date), '%Y-%m-%d') < datetime.datetime.today() - timedelta:
                return
            element = model.Element(title=str(text[0][2:]), date = date, url=str(href[0]))
            exist = element.check_exist()
            #If this element doesn`t exist in the database, it means this is a new element.
            # if exist == False:
            #    element.set_date(datetime.date.today())
            element.save()


