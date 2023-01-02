# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from hashlib import sha256


class GraphPipeline:
    def process_item(self, item, spider):
        return item


class LinkPipeline:
    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        hash = sha256()
        for k in ['source', 'target']:
            hash.update(bytes(k + repr(adapter[k]), encoding='UTF-8'))
        digest = hash.digest()
        if digest in self.seen:
            raise DropItem(f'Duplicate item found: {item!r}')
        else:
            self.seen.add(digest)
            return item
