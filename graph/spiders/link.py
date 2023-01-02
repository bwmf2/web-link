import scrapy


class LinkSpider(scrapy.Spider):
    name = 'link'

    def __init__(self, urls, skips='', data='hostname', *args, **kwargs):
        super(LinkSpider, self).__init__(*args, **kwargs)
        self.start_urls = urls.split(',')
        self.skips = skips.split(',')
        self.data = data

    def parse(self, response):
        pass
