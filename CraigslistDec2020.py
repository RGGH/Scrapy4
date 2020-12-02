#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# Craigslist Scrapy Project #
''' Scrapes approx 3000 Properties on Craigslist
    and gets geo data from details page '''
    
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Request

class RealestateSpider(scrapy.Spider):

    name = 'realestate_loader'
    custom_settings = {"FEEDS": {"results.csv": {"format": "csv"}},'CONCURRENT_REQUESTS': 5}

    start_urls = ['http://newyork.craigslist.org/d/real-estate/search/rea/']
    try:
        os.remove('results.csv')
    except OSError:
        pass

    def start_requests(self):
         yield scrapy.Request('http://newyork.craigslist.org/d/real-estate/search/rea/', callback=self.parse)

    def parse(self,response):

        all_ads = response.xpath('//div[@class="result-info"]')
        for ads in all_ads:

            price = ads.xpath(".//span[@class='result-price']/text()").get()
            date = ads.xpath(".//time[@class='result-date']/text()").get()
            title = ads.xpath(".//a[@class='result-title hdrlnk']/text()").get()
            hood = ads.xpath(".//span[@class='result-hood']/text()").get()
            details_link = ads.xpath(".//a[@class='result-title hdrlnk']/@href").get()

            # call parse_details and pass all of the above to it
            request = Request(url=details_link,callback=self.parse_detail, cb_kwargs={
            'price': price, 
            'date': date, 
            'title':title,
            'hood':hood,
            'details_link':details_link
            })
            
            yield request

        # Get the next 25 properties from 'next page' - persist until no more #
        next_page = response.xpath("//a[@class='button next']/@href").get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)


    
    def parse_detail(self,response,price, date,title,hood,details_link):

        lon = response.xpath('//meta[@name="geo.position"]/@content').get().split(";")[0]
        lat = response.xpath('//meta[@name="geo.position"]/@content').get().split(";")[1]

        yield{
            'price': price, 
            'date': date, 
            'title':title,
            'hood':hood,
            'details_link':details_link,
            'lon':lon,
            'lat':lat
            }

# main driver #
if __name__ == "__main__" :
    # Create Instance called 'cl' as in "c"raigs "l"ist
    cl = CrawlerProcess()
    cl.crawl(RealestateSpider)
    cl.start()
