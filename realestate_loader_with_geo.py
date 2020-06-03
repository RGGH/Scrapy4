#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Craigslist Scrapy Project #
import os
import scrapy
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from items import CraigslistItem
from urllib.parse import urljoin
import requests
import time

class RealestateSpider(scrapy.Spider):

    name = 'realestate_loader'
    #allowed_domains = ['newyork.craigslist.org/d/real-estate/search/rea']
    start_urls = ['http://newyork.craigslist.org/d/real-estate/search/rea/']
    try:
        os.remove('results.csv')
    except OSError:
        pass

    def __init__(self):
        self.lat =""
        self.lon = ""

    def start_requests(self):
         yield scrapy.Request('http://newyork.craigslist.org/d/real-estate/search/rea/', callback=self.parse)

    def parse(self,response):

        all_ads = response.xpath('//p[@class="result-info"]')
        for ads in all_ads:
            #details_link = ads.xpath(".//a[@class='result-title hdrlnk']/@href").getall()
            details_link = ads.xpath(".//a[@class='result-title hdrlnk']/@href").get()
            # get GEO data from details link #
            #self.parse_detail(details_link)
            yield response.follow(url=details_link, callback=self.parse_detail)
        #####################################
        loader = ItemLoader(item=CraigslistItem(),selector = ads,response=response)
        loader.add_xpath("price",".//span[@class='result-price']/text()")
        loader.add_xpath("date",".//time[@class='result-date']/text()")
        loader.add_xpath("title",".//a[@class='result-title hdrlnk']/text()")
        loader.add_xpath("hood",".//span[@class='result-hood']/text()")
        loader.add_xpath("details_link",".//a[@class='result-title hdrlnk']/@href")
        loader.add_value("lon",self.lon)
        loader.add_value("lat",self.lat)
        yield loader.load_item()
        #####################################
        next_page = response.xpath("//a[@class='button next']/@href").get()
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse)

    # Drop down to details level to extract the Geo coordinates #
    #<meta name="detail.position" content="40.578355;-73.959875">#
    def parse_detail(self,response):

        #yield scrapy.Request(details_link, callback = self.parse_list)
        self.lon = response.xpath('//meta[@name="geo.position"]/@content').get().split(";")[0]
        self.lat = response.xpath('//meta[@name="geo.position"]/@content').get().split(";")[1]

# main driver #
if __name__ == "__main__" :

    cl = CrawlerProcess(settings={
    "FEEDS": {
        "results.csv": {"format": "csv"},
    },
    })

    cl.crawl(RealestateSpider)
    cl.start()
