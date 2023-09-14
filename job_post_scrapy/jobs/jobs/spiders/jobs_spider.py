import scrapy


class JobsSpiderSpider(scrapy.Spider):
    name = "jobs_spider"
    allowed_domains = ["linkedin.com"]
    start_urls = ["http://linkedin.com/"]

    def parse(self, response):
        pass
