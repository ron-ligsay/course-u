import scrapy


class JobsSpiderSpider(scrapy.Spider):
    name = "jobs_spider"
    allowed_domains = ["linkedin.com"]
    #base_urls = ["http://linkedin.com/"]
    location = "Philippines"
    keywords = ["software development","data and analytics","dasign and ui/ux","testing and quality assurance","networking and infrastructure"]
    start_urls = ["https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?location=Philippines&keywords=" + str(keyword) for keyword in keywords ]

    def start_requests(self):
        for keyword in self.keywords:
            yield scrapy.Request(url="https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?location=Philippines&keywords=" + str(keyword), callback=self.parse, meta={'keyword': keyword})

    def parse(self, response):
        jobs = response.css('div.job-search-card')

        for job in jobs:
            item = {
                'link' : job.css('a.base-card__full-link ::attr(href)').get(),
                'keyword' : response.meta['keyword'], 
                'title' : job.css('h3::text').get().strip(),
                'company' : job.css('a.hidden-nested-link::text').get().strip(),
                'company_link' : job.css('a.hidden-nested-link::attr(href)').get(),
                'date' : job.css('time::attr(datetime)').get()
            }
            yield item

        pass
