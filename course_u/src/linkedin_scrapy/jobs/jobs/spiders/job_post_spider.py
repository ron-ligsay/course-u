import scrapy


class JobPostSpiderSpider(scrapy.Spider):
    name = "job_post_spider"
    allowed_domains = ["ph.linkedin.com"]
    start_urls = ["http://ph.linkedin.com/"]

    def parse(self, response):
        pass
