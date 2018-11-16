import scrapy
import json
import datetime
import sys
sys.path.append('../')
from database import model

class IndieGameNewsSpider(scrapy.Spider):
    name =  "mightyvision"
    def start_requests(self):
        urls = [
            'http://mightyvision.blogspot.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url , callback=self.parse)

    def formatTime(self, raw):
        sp = raw.split(',')[1].split(' ')
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
        return datetime.date(int(year) , int(m[month]) , int(day))

    def parse(self, response):
        list = response.css('.date-outer')
        for item in list:
            date_header = item.css('.date-header span ::text').extract()
            if (len(date_header) <=0):
                continue
            date_info = date_header[0]
            date = self.formatTime(date_info)
            title_dom = item.css('h3[class = "post-title entry-title"] a')
            if (len(title_dom)<=0):
                continue
            url = title_dom.css("::attr(href)").extract()[0]
            title = title_dom.css("::text").extract()[0]
            element = model.Element(title=title , date = date , url=url)
        #Parse the next url.
        next_url = response.css('.blog-pager-older-link ::attr(href)').extract()
        if(next_url):
            yield scrapy.Request(url=next_url[0], callback=self.parse)