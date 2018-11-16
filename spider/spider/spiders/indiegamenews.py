import scrapy
import json
import datetime
import sys

sys.path.append('../')
from database import model
from scrapy.exceptions import CloseSpider


# 因技术原因 暂时只能爬本月的
class IndieGameNews(scrapy.Spider):
    name = "indiegamenews"
    index = 0
    urls = []

    def start_requests(self):
        urls = [
            'http://www.indiegamenews.com'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.getURLs)

    # raw is a string like " • March 24, 2011"
    def formatTime(self, raw):
        sp = raw.split(' ')
        year = sp[3]
        month = sp[2]
        day = sp[1]
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
        return datetime.date(int(year), int(m[month]), int(day))

    def getURLs(self, response):
        lis = response.css("div[id='BlogArchive1_ArchiveList']").css("a")
        for li in lis:
            href = li.css('::attr(href)').extract()[0]
            if (href.find("html") != -1):
                self.urls.append(href)
        yield scrapy.Request(url=self.urls[0], callback=self.parse)

    def parse(self, response):
        href = response.url
        title = response.css("h3[class='post-title entry-title']::text").extract()[0].strip()
        rawTime = response.css("h2[class='date-header']").css("span::text").extract()[0]
        date = self.formatTime(rawTime)
        print('\033[1;35m {} {} {} \033[0m'.format(href, title, date))
        # 爬取整站时关闭，每天更新时将下面两句取消注释
        # if(date != datetime.date.today()):
        #     raise CloseSpider("{name}没有新的更新".format(name=self.name))
        element = model.Element(title=title, date=date, url=href)
        element.save()
        if (self.index + 1 < len(self.urls)):
            self.index += 1
            yield scrapy.Request(url=self.urls[self.index], callback=self.parse)
