import scrapy
from scrapy.loader import ItemLoader
from COVID_Webscraper.items import CovidWebscraperItem

# A spider that crawls the worldometers website
class CovidSpider(scrapy.Spider):
    
    name = 'cases'
    allowed_domains = ['www.worldometers.info/coronavirus/']
    start_urls = ['https://www.worldometers.info/coronavirus/']

    # Uses xml paths to recover current country cases, recoveries, and population
    def parse(self, response):
        
        cases = response.xpath('//tr')[9:]
        for case in cases:
            loader = ItemLoader(item=CovidWebscraperItem(), selector=case)
            
            # Stops collecting data after all countries data is collected
            if case.xpath('.//td[1]//text()').get() is None:
                break
            loader.add_xpath('country_name', './/td[2]//text()')
            loader.add_xpath('total_recoveries', './/td[7]')
            loader.add_xpath('total_active_cases', './/td[9]//text()')
            loader.add_xpath('population', './/td[15]//text()')

            # Returns items after removing unnecessary tags and commas
            yield loader.load_item()
