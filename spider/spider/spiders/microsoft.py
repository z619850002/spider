import scrapy
import json
import datetime
import sys

sys.path.append('../')
from database import model
import json


class MicrosoftSpider(scrapy.Spider):
    name = "microsoft"

    def start_requests(self):
        urls = [
            'https://microsoftdesign-service.azurewebsites.net/api/articles',
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
        res = json.loads(response.body)
        items = res["items"]
        for (k, v) in items.items():
            href = v['link']
            href = href[:href.find('?source')]
            title = v['title']
            rawTime = v['date']
            date = self.formatTime(rawTime)
            # 这个网站上时间是乱序的，不过文章数量不多，就每次都爬整站了
            # print(href, title, date)
            element = model.Element(title=title, date=date, url=href)
            element.save()
