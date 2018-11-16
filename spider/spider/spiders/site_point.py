import scrapy
import json
import datetime
import sys
import json

sys.path.append('../')
from database import model


class SitePointSpider(scrapy.Spider):
    name = "sitepoint"

    def start_requests(self):
        urls = [
            'https://www.sitepoint.com/janus/api/LatestArticle/8/0/All',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def formatTime(self, raw):
        sp = raw[:10].split('-')
        year = sp[0]
        month = sp[1]
        day = sp[2]
        return datetime.date(int(year), int(month), int(day))

    def parse(self, response):
        infos = json.loads(response.body)
        status = response.status
        for info in infos:
            href = info['url']
            title = info['title']
            rawTime = info['publish_date']
            date = self.formatTime(rawTime)
            timedelta = datetime.timedelta(days=3)
            if datetime.datetime.strptime(str(date), '%Y-%m-%d') < datetime.datetime.today() - timedelta:
                return
            # print(href, title, date)
            element = model.Element(title=title, date=date, url=href)
            element.save()
        if (status == 200):
            currURL = response.url
            index = int(currURL.split('/')[-2]) + 8
            nextURL = 'https://www.sitepoint.com/janus/api/LatestArticle/8/{s}/All'.format(s=index)
            yield scrapy.Request(url=nextURL, callback=self.parse)
