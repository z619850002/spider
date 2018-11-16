import scrapy
import json
import datetime
import sys

sys.path.append('../')
from database import model
from termcolor import *

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class ScheduleSpider(scrapy.Spider):
    name = "schedule"

    def start_requests(self):
        yield scrapy.Request(url='http://schedule.gdconf.com/sessions', callback=self.parse)

    def parse(self, response):
        print(colored("begin to parse!", 'red'))
        articles=response.css("div[class='sb5-session-detail row']")
        print(colored("Get articles" , "red"))
        for article in articles:
            url=article.css("p[class='sb5-session-title'] a::attr(href)").extract_first()
            print(colored("get url" , "red"))
            title=article.css("p[class='sb5-session-title'] a::text").extract_first()
            print(colored("get title" , "red"))
            timestr=article.css("p[class='sb5-time'] time::text").extract_first()
            strs = timestr.split()
            months = ('january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                      'november', 'december')
            date = datetime.datetime(year=2018, month=(months.index(strs[1].lower()) + 1), day=int(strs[2]))
            print(colored(date,'red'))
            element = model.Element(title=title, date=date, url=url)
            element.save()
