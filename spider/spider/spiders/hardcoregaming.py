import scrapy
import json
import datetime
import sys

sys.path.append('../')
from database import model
import json


class MicrosoftSpider(scrapy.Spider):
    name = "hardcoregaming"

    def start_requests(self):
        urls = [
            'http://www.hardcoregaming101.net/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def formatTime(self, raw):
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

        sp = raw[1:].replace(',', '').split(' ')
        month = m[sp[0].replace(' ','')]
        day = sp[1].replace(' ','')
        year = sp[2].replace(' ','')
        return datetime.date(int(year), int(month), int(day))

    def parse(self, response):
        doms = response.css('.index-posts .with-featured-image')
        for item in doms:
            date_info = item.css('.entry-byline-date ::text').extract()[0]
            date = self.formatTime(date_info)
            title_dom = item.css('.entry-title a')
            title = title_dom.css('::text').extract()[0]
            url = title_dom.css('::attr(href)').extract()[0]
            element = model.Element(title=title, date=date, url=url)
            element.save()






