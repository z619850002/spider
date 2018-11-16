import scrapy
import json
import datetime
import sys
from termcolor import *


sys.path.append('../')
from database import model


class GraphisBlogSpider(scrapy.Spider):
    name = "graphis"

    def start_requests(self):
        base_url ='http://blog.graphis.com/page/'
        urls = []
        for i in range(50):
            url = base_url + str(i) + '/'
            urls.append(url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):
        articles = response.css("div[id^='post-']")
        if len(articles) <=0:
            return
        for li in articles:
            title = li.css("h2[class = 'posttitle'] a ::text").extract()[0][2:]
            url = li.css("h2[class='posttitle'] a ::attr(href)").extract()[0]
            #Date need to be parsed in another page.
            request = scrapy.Request(url = url , callback= self.parse_date)
            request.meta['title'] = title
            request.meta['url'] = url
            yield request


    def parse_date(self , response):
        date_info = response.css("li[class = 'datemeta'] ::text").extract()[0]
        date = self.get_date(date_info=date_info)
        timedelta = datetime.timedelta(days=3)
        if datetime.datetime.strptime(str(date),'%Y-%m-%d') < datetime.datetime.today() - timedelta:
            return
        title = response.meta['title']
        url = response.meta['url']
        print(colored(date , "red"))
        print(colored(title , "red"))
        element = model.Element(title=title , url=url , date=date)
        element.save()


    def get_date(self , date_info):
        date = datetime.datetime.today()
        time_value = int(date_info.split(' ')[0])
        time_delta = datetime.timedelta()
        if 'second' in date_info:
            time_delta = datetime.timedelta(seconds=time_value)
        elif 'minute' in date_info:
            time_delta = datetime.timedelta(minutes=time_value)
        elif 'hour' in date_info:
            time_delta = datetime.timedelta(hours=time_value)
        elif 'day' in date_info:
            time_delta = datetime.timedelta(days=time_value)
        elif 'week' in date_info:
            time_delta = datetime.timedelta(weeks=time_value)
        date = date - time_delta
        year = date.year
        month = date.month
        if 'month' in date_info:
            month -= time_value
            while month < 1:
                month += 12
                year -= 1
        if 'year' in date_info:
            year -= time_delta

        date_res = datetime.date(year= year , month= month , day= date.day)
        return date_res