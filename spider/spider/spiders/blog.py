import scrapy
import sys
sys.path.append('../')
from database import model
import datetime

m = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


class BlogSpider(scrapy.Spider):
    name = "blog"

    def start_requests(self):
        urls = [
            'https://heydesigner.com/blog/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        element = response.css('li').css('h3').css('a')
        for item in element:
            href = item.css('::attr(href)').extract()
            text = item.css('::text').extract()
            request = scrapy.Request(url=href[0], callback=self.parse2)
            request.meta['text'] = text
            request.meta['href'] = href
            yield request

    def parse2(self, response):
        element = response.css('header').css('div').css('p')
        text = element[0].css('::text').extract()
        date = datetime.datetime.strptime(self.get_date(text[len(text) - 1]) , '%Y-%m-%d')
        timedelta = datetime.timedelta(days=3)
        if date < datetime.datetime.today() - timedelta:
            return
        url = response.meta['href'][0]
        title = response.meta['text'][0]
        element = model.Element(title=title, date=date, url=url)
        element.save()

    def get_date(self, text):
        for mouth in m:
            index = text.rfind(mouth)
            if index != -1:
                return self.turn_format(text[index:])
        return "no date !"

    def turn_format(self, date):
        l = date.split(' ')
        for i in range(len(m)):
            if l[0].rfind(m[i]) != -1:
               mouth = i+1
        day = l[1][0:len(l[1])-1]
        year = l[2]
        return year + '-' + str(mouth) + '-' + day