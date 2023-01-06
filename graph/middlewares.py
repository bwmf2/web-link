# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import scrapy
from scrapy import signals
import logging
from urllib.parse import urlparse

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


logger = logging.getLogger(__name__)


class GraphSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LocalDepthMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, local_depth):
        self.local_depth = local_depth

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        settings = crawler.settings
        local_depth = settings.getint('LOCAL_DEPTH')
        return cls(local_depth)

    def process_spider_output(self, response, result, spider):
        if self.local_depth == 0:
            return (r for r in result or ())
        else:
            self._init_depth(response, spider)
            return (
                r for r in result or () if self._filter(r, response, spider)
            )

    async def process_spider_output_async(self, response, result, spider):
        if self.local_depth == 0:
            async for r in result or ():
                yield r
        else:
            self._init_depth(response, spider)
            async for r in result or ():
                if self._filter(r, response, spider):
                    yield r

    def _init_depth(self, response, spider):
        # base case (depth=0)
        if 'local_depth' not in response.meta:
            logger.debug(
                'Initialize link (local): %(url)s',
                {'url': response.url},
                extra={'spider': spider},
            )
            response.meta['local_depth'] = 0

    def _filter(self, request, response, spider):
        response_domain = urlparse(response.url).netloc
        if not isinstance(request, scrapy.Request):
            return True
        request_domain = urlparse(request.url).netloc
        depth = response.meta['local_depth']
        if request_domain == response_domain:
            depth += 1
        else:
            depth = 0
        request.meta['local_depth'] = depth
        if self.local_depth and depth >= self.local_depth:
            logger.debug(
                "Ignoring link (local_depth >= %(l_depth)d): %(req_url)s ",
                {'l_depth': self.local_depth, 'req_url': request.url},
                extra={'spider': spider},
            )
            return False
        return True


class GlobalDepthMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, global_depth):
        self.global_depth = global_depth

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        global_depth = settings.getint('GLOBAL_DEPTH')
        return cls(global_depth)

    def process_spider_output(self, response, result, spider):
        if self.global_depth == 0:
            return (r for r in result or ())
        else:
            self._init_depth(response, spider)
            return (
                r for r in result or () if self._filter(r, response, spider)
            )

    async def process_spider_output_async(self, response, result, spider):
        if self.global_depth == 0:
            async for r in result or ():
                yield r
        else:
            self._init_depth(response, spider)
            async for r in result or ():
                if self._filter(r, response, spider):
                    yield r

    def _init_depth(self, response, spider):
        # base case (depth=0)
        if 'global_depth' not in response.meta:
            logger.debug(
                'Initialize link (global): %(url)s',
                {'url': response.url},
                extra={'spider': spider},
            )
            response.meta['global_depth'] = 0

    def _filter(self, request, response, spider):
        response_domain = urlparse(response.url).netloc
        if not isinstance(request, scrapy.Request):
            return True
        request_domain = urlparse(request.url).netloc
        depth = response.meta['global_depth']
        if request_domain != response_domain:
            depth += 1
        request.meta['global_depth'] = depth
        if self.global_depth and depth >= self.global_depth:
            logger.debug(
                "Ignoring link (global_depth >= %(g_depth)d): %(req_url)s ",
                {'g_depth': self.global_depth, 'req_url': request.url},
                extra={'spider': spider},
            )
            return False
        return True
