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



class SmashSpider(scrapy.Spider):
    name =  "smash"
    def start_requests(self):

        urls = [
            'https://www.smashingmagazine.com/articles/page/1/',
        ]
        for url in urls:
            yield scrapy.Request(url=url , callback=self.parse)

    def parse(self , response):
        base_url = "https://www.smashingmagazine.com"

        body = response.css('main section')
        res = body.css('nav ul')
        res2 = res.css('.pagination__next')
        urlDomLen = len(res2.css('a ::attr(href)'))
        if (urlDomLen != 1):
            return
        nextPageUrl = base_url + res2.css('a ::attr(href)')[0].extract()
        elements = body.css('.container .row .col article')
        #Get the date of yesterday, article before yesterday needn`t update.
        one_day = datetime.timedelta(days=1)
        yesterday = datetime.datetime.today() - one_day
        for item in elements:
            #Get the dom stores the title and the url.
            title_dom = item.css('h1 a')
            url = base_url + title_dom.css('::attr(href)').extract()[0]
            title = title_dom.css('::text').extract()[0]
            #Get the dom stores the date.
            date_dom = item.css('.article--post__content ')
            date = datetime.datetime.strptime(date_dom.css('time ::attr(datetime)').extract()[0] , '%Y-%m-%d')
            timedelta = datetime.timedelta(days=3)
            if date < datetime.datetime.today() - timedelta:
                return
            element = model.Element(title=title , date=date , url=url)
            print([title , date , url])
            element.save()
        #Call for the next page
        yield scrapy.Request(url = nextPageUrl , callback = self.parse)

