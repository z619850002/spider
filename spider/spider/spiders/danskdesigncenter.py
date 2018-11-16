import scrapy
import json
import datetime
import sys

sys.path.append('../')
from database import model
from termcolor import *

class DesignModoSpider(scrapy.Spider):
    name = "danskdesigncenter"
    baseurl = "https://danskdesigncenter.dk"

    def start_requests(self):
        urls = [
            'https://danskdesigncenter.dk/en/articles',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def formatTime(self, raw):
        raw = raw.replace('.' , '')
        sp = raw.split(' ')
        year = sp[-1]
        month = sp[-2]
        day = sp[-3]
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
        doms = response.css("article[class = 'node node-article view-mode-teaser-small clearfix']")
        for item in doms:
            url = self.baseurl + item.css("a ::attr(href)").extract()[0]
            title_list = item.css(".text div[class = 'field title-field'] .item ::text").extract()
            title_str = ""
            for title_item in title_list:
                title_str = title_str + title_item
            title = title_str

            #Get the date.
            request = scrapy.Request(url=url, callback=self.parse2)
            request.meta['title'] = title
            request.meta['url'] = url
            yield request


    def parse2(self , response):
        date_info = response.css('.timestamp ::text').extract()[0]
        date = self.formatTime(date_info)
        url = response.meta['url']
        title = response.meta['title']
        element = model.Element(title=title, date=date, url=url)
        element.save()
        print(colored(date , 'red'))