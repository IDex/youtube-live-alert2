import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class YtchanSpider(CrawlSpider):
    name = 'ytchan'
    allowed_domains = ['example.com']
    start_urls = ['']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        [re.findall(r'"(.*?)":(".*?"|\[.*?\]|true|false)', x) for x in re.findall(r'videoDetails":{(.*?)}',response.text)]
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
