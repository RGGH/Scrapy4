# -*- coding: utf-8 -*-
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# Craigslist Scrapy Project  - CSS example
import scrapy
from ..items import CraigslistItem

class RealestateSpider(scrapy.Spider):
    name = 'realestate'
    allowed_domains = ['newyork.craigslist.org/d/real-estate/search/rea']
    start_urls = ['http://newyork.craigslist.org/d/real-estate/search/rea/']

    def parse(self, response):
        print("\n")
        print("HTTP STATUS: "+str(response.status))
        print(response.css("title::text").get())
        print("\n")

    def parse(self,response):
        all_ads = response.css("p.result-info")

        for ads in all_ads:
            date = ads.css("time.result-date::text").get()
            title = ads.css("a.result-title.hdrlnk::text").get()
            price = ads.css("span.result-price::text").get()
            hood = ads.css("span.result-hood::text").get()
            link = ads.css("a.result-title.hdrlnk::attr(href)").get()

            print("====NEW PROPERTY===")
            print(date)
            print(title)
            print(price)
            print(hood)
            print(link)

            items = CraigslistItem()

            items['date'] = date
            items['title'] = title
            items['price'] = price
            items['hood'] = hood
            items['link'] = link

            yield items
