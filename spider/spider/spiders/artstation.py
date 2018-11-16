import scrapy
import json
import datetime
import sys

sys.path.append('../')
from database import model
import json
from termcolor import *


class AirbnbSpider(scrapy.Spider):
    name = "artstation"

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

        sp = raw.replace(',', '').split(' ')
        month = m[sp[0].replace(' ','')]
        day = sp[1].replace(' ','')
        year = sp[2].replace(' ','')
        return datetime.date(int(year), int(month), int(day))


    def start_requests(self):
        urls = [
            "https://magazine.artstation.com/category/inspiration/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):

        divs = response.css('.small-archive-item')

        for item in divs:
            #Dom contains the information of title.
            title_dom = item.css('.archive-panel')
            #title.
            title = title_dom.css('h4 a ::text').extract()[0]
            url = title_dom.css('h4 a ::attr(href)').extract()[0]

            #No date in the website, so I need to use today as the date, the code here need to change in the future.
            raw_data = item.css('.byline ::text')[2].extract()[3:]
            date = self.formatTime(raw_data)
            timedelta = datetime.timedelta(days=3)
            if datetime.datetime.strptime(str(date), '%Y-%m-%d') < datetime.datetime.today() - timedelta:
                return


            element = model.Element(title = title , url= url , date = date)
            element.save()
            print(colored(date , 'red'))

        next_dom = response.css("div[class = 'col-xs-6 text-right next-posts-link'] a ::attr(href)").extract()
        if (len(next_dom) <=0):
            return
        nexturl = next_dom[0]
        yield scrapy.Request(url=nexturl, callback=self.parse)
