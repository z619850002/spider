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


class GamescenesSpider(scrapy.Spider):
    name = "gamescenes"

    def start_requests(self):
        urls = [
            'https://www.gamescenes.org/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        articles = response.xpath("//div[@class='entry-inner']/h3[@class='entry-header']/a")
        # 获取下一页的超链接
        nextPageUrl = response.xpath("//span[@class='pager-right']/a/@href").extract_first(default="NO NEXTPAGE")
        if nextPageUrl == "NO NEXTPAGE":
            return
        else:
            nextPageUrl = nextPageUrl

        for article in articles:
            # 解析文章标题
            title = article.xpath("text()").extract_first(default="NO TITLE")
            # 解析文章超链接
            url = article.xpath("@href").extract_first(default="NO URL")
            # 打开文章url，查询日期
            request = scrapy.Request(url, callback=self.parse2)
            # 发送数据
            request.meta['title'] = title
            request.meta['url'] = url
            yield request
        # Call for the next page
        yield scrapy.Request(url=nextPageUrl, callback=self.parse)

    def parse2(self, response):
        # 获得日期
        dateStr = response.xpath("//h2[@class='date-header']").xpath("text()").extract_first().split('/')
        date = datetime.datetime(year=int(dateStr[2]), month=int(dateStr[0]), day=int(dateStr[1]))
        # 接受文章标题和文章超链接数据
        title = response.meta['title']
        url = response.meta['url']

        timedelta = datetime.timedelta(days=3)
        #if datetime.datetime.strptime(str(date), '%Y-%m-%d') < datetime.datetime.today() - timedelta:
        #    return
        print(colored(date , 'red'))

        # 保存数据
        element = model.Element(title=title, date=date, url=url)
        element.save()
