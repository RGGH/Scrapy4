#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# Craigslist Scrapy Project # - CSS example with Item Loader
import scrapy
from scrapy.loader import ItemLoader
from ..items import CraigslistItem

class RealestateSpider(scrapy.Spider):
    name = 'realestate_loader'
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

            loader = ItemLoader(item=CraigslistItem(),
                selector=ads, response=response)

            loader.add_css("date","time.result-date::text")
            loader.add_css("title","a.result-title.hdrlnk::text")
            loader.add_css("price","span.result-price::text")
            loader.add_css("hood","span.result-hood::text")
            loader.add_css("link","a.result-title.hdrlnk::attr(href)")
            loader.add_value("misc", "DEMO")
            # print("====NEW PROPERTY===")
            # print(date)
            # print(title)
            # print(price)
            # print(hood)
            # print(link)

            #items = CraigslistItem()

            # items['date'] = date
            # items['title'] = title
            # items['price'] = price
            # items['hood'] = hood
            # items['link'] = link

            yield loader.load_item()
