import scrapy


class LinkSpider(scrapy.Spider):
    name = 'link'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        pass
