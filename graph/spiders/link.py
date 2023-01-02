from urllib.parse import urlparse
import scrapy
from graph.items import EdgeItem


class LinkSpider(scrapy.Spider):
    name = 'link'

    def __init__(self, urls, skips='', data='hostname', *args, **kwargs):
        super(LinkSpider, self).__init__(*args, **kwargs)
        self.start_urls = urls.split(',')
        self.skips = skips.split(',')
        self.data = data

    def parse(self, response):
        if self.data == 'hostname':
            extract = lambda url: urlparse(url).hostname
        elif self.data == 'domain':
            extract = lambda url: urlparse(url).netloc
        else:
            raise ValueError(
                'Unknown data requested: {}'.format(repr(self.data))
            )

        source = extract(response.url)
        for next_page in response.xpath('//a/@href'):
            try:
                request = response.follow(next_page, self.parse)
                request.meta['dont_redirect'] = True
            except ValueError:
                continue

            target = extract(request.url)
            if target in self.skips:
                continue
            yield request

            item = EdgeItem()
            item['source'] = source
            item['target'] = target
            yield item
