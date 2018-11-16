import scrapy
import json
import datetime
import sys
from termcolor import *


sys.path.append('../')
from database import model


DATE_DICT = {
    'January' : 1,
    'February' :2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
}

class UxmagSpider(scrapy.Spider):
    name = "uxmag"

    def start_requests(self):
        urls = [
            "http://uxmag.com/articles",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse_date(self , date_str):
        year = int(date_str.split(',')[1].replace(' ',''))
        date_str = date_str.split(',')[0]
        day = int(date_str.split('  ')[1])
        month = DATE_DICT[date_str.split('  ')[0].replace(' ','')]
        date = datetime.date(year=year , month=month , day=day)
        return date

    def parse(self, response):
        base_url = "http://uxmag.com"
        doms = response.css(".views-row")
        for item in doms:
            date_info = item.css("div[class = 'views-field views-field-created'] span ::text").extract()[0].split('|')[1]
            date = self.parse_date(date_info)
            timedelta = datetime.timedelta(days=3)
            if datetime.datetime.strptime(str(date), '%Y-%m-%d') < datetime.datetime.today() - timedelta:
                return
            print(colored(date , "red"))
            title_dom = item.css("div[class = 'views-field views-field-title']")
            url = base_url + title_dom.css("a ::attr(href)").extract()[0]
            title = title_dom.css("h2 ::text").extract()[0]
            element = model.Element(title=title , url=url , date=date)
            element.save()


        #Parse for the next page.
        next_dom = response.css(".pager-next a ::attr(href)")
        if len(next_dom) <=0:
            return
        next_url = base_url + response.css(".pager-next a ::attr(href)").extract()[0]
        yield scrapy.Request(url=next_url, callback=self.parse)

