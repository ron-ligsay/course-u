# import scrapy


# class JobsApiSpider(scrapy.Spider):
#     name = "jobs_api"
#     allowed_domains = ["linkedin.com"]
#     start_urls = ["http://linkedin.com/"]

#     def parse(self, response):
#         pass

import scrapy

class JobsApiSpider(scrapy.Spider):
    name = "jobs_api"
    allowed_domains = ["linkedin.com"]
    location = ["Philippines"]
    keywords = [
        "software development", "data and analytics", "design and ui/ux",
        "testing and quality assurance", "networking and infrastructure"
    ]
    PAGES = 5

    def start_requests(self):
        for location in self.location:
            for keyword in self.keywords:
                for page in range(self.PAGES):
                    url = self.build_url(location, keyword, page)
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse,
                        meta={'location': location, 'keyword': keyword, 'page': page}
                    )

    def parse(self, response):
        location = response.meta['location']
        keyword = response.meta['keyword']
        page = response.meta['page']

        jobs = response.css('div.job-search-card')

        for job in jobs:
            item = self.extract_job_data(job, keyword)
            yield item

            log_message = self.format_log_message(item)
            self.log_to_file(log_message)

        log_message = self.format_page_log_message(location, keyword, page, response.url)
        self.log_to_file(log_message)

    def build_url(self, location, keyword, page):
        start = page * 25  # Each page contains 25 jobs
        return f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?location={location}&keywords={keyword}&start={start}"

    def extract_job_data(self, job, keyword):
        return {
            'link': self.clean_link(job.css('a.base-card__full-link ::attr(href)').get()),
            'keyword': keyword,
            'title': job.css('h3::text').get().strip(),
            'company': job.css('a.hidden-nested-link::text').get().strip(),
            'company_link': self.clean_link(job.css('a.hidden-nested-link::attr(href)').get()),
            'date': job.css('time::attr(datetime)').get(),
        }

    def clean_link(self, link):
        if link:
            parts = link.split('&')
            if parts:
                first_part = parts[0]
                return first_part.replace('ph.', '')
        return None

    def format_log_message(self, item):
        return f"Scraped job - Title: {item['title']}, Company: {item['company']}"

    def format_page_log_message(self, location, keyword, page, url):
        return f"Location: {location}, Keyword: {keyword}, Page: {page}, URL: {url}"

    def log_to_file(self, message):
        with open('log.txt', 'a') as f:
            f.write(message + '\n')
