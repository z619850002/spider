import scrapy
import json
import datetime
import sys
sys.path.append('../')
from database import model
import string
from termcolor import *


DATE_DICT = {
    'January ' : 1,
    'February ' :2,
    'March ': 3,
    'April ': 4,
    'May ': 5,
    'June ': 6,
    'July ': 7,
    'August ': 8,
    'September ': 9,
    'October ': 10,
    'November ': 11,
    'December ': 12,
}



class UxBoothSpider(scrapy.Spider):
    name =  "uxbooth"
    def start_requests(self):

        urls = [
            'http://www.uxbooth.com/articles/page/20/',
        ]
        for url in urls:
            yield scrapy.Request(url=url , callback=self.parse)

    def parse(self , response):
        base_url = "http://www.uxbooth.com"
        #Firstly get the next page url.
        container = response.css('.article-archive .page-body .wrapper')
        container = container.css('.page-body__inner .page-body__layout .page-body__primary')
        article_container = container.css('.articles')

        articles = article_container.css('article')

        for item in articles:
            url = item.css('a ::attr(href)').extract()[0]
            title = item.css('a h1 ::text').extract()[0].replace('  ','').replace('\n','')
            date_str = item.css('.articles__article-meta ::text').extract()[0].replace('  ','').replace('\n','')
            #Example, 'Amy Grace Wells &bullet; October 2nd, 2018'
            day = 1
            month = 1
            year = 2018
            for item2 in DATE_DICT.keys():
                if date_str.rfind(item2)!=-1:
                    date_str = date_str[date_str.rfind(item2):]
                    #Get the month.
                    month = DATE_DICT[item2]
                    #Get the day.
                    day = int(date_str[len(item2):date_str.rfind(',')-2].replace(' ',''))
                    #Get the year.
                    year = int(date_str[date_str.rfind(',')+1:].replace(' ',''))
                    break
            #Set the date.
            date = datetime.date(year = year , month=month , day=day)
            print(colored(date,'red'))
            timedelta = datetime.timedelta(days=3)
            if date < datetime.date.today() - timedelta:
                return      
            element = model.Element(title=title , url=url , date = date)
            element.save()




        container = container.css('.pagination')
        #Get the ul.
        ulist = container.css('ul li')
        current_page = ulist.css('.pagination__link--current')

        #Get the index of the next page button.
        list_obj = ulist.css('a').extract()
        current_page_obj = current_page.extract()

        current_page_index = -1

        for index , item in enumerate(list_obj):
            if item == current_page_obj[0]:
                current_page_index = index

        if current_page_index ==-1:
            return

        next_page_index = current_page_index+1
        if (next_page_index > len(list_obj)):
            return
        #Get the url of the next page.
        next_page_url = base_url + ulist.css('a')[next_page_index].css('::attr(href)').extract()[0]
        yield scrapy.Request(url = next_page_url , callback = self.parse)
