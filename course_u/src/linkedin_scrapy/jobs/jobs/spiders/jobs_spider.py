import scrapy


class JobsSpiderSpider(scrapy.Spider):
    name = "jobs_spider"
    allowed_domains = ["linkedin.com"]
    # base_urls = ["http://linkedin.com/"]
    location = ["Philippines"]
    keywords = [
        "software development","data and analytics","dasign and ui/ux",
        "testing and quality assurance","networking and infrastructure"
        ]
    
    PAGES = 5
    

    start_urls = ["https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?location=Philippines&keywords=" + str(keyword) for keyword in keywords ]


    def start_requests(self):
        for location in self.location:
            for keyword in self.keywords:
                for page in range(self.PAGES):
                    start = page * 25 # each page contains 25 jobs
                    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?location={location}&keywords={keyword}&start={start}"
                    yield scrapy.Request(
                        url= url, 
                        callback=self.parse, 
                        meta={'location' : location,'keyword': keyword, 'page' : page}
                    )

    def parse(self, response):
        location = response.meta['location']
        keyword = response.meta['keyword']
        page = response.meta['page']

        jobs = response.css('div.job-search-card')

        for job in jobs:
            item = {
                
                'link' : job.css('a.base-card__full-link ::attr(href)').get(),
                'keyword' : response.meta['keyword'], 
                'title' : job.css('h3::text').get().strip(),
                'company' : job.css('a.hidden-nested-link::text').get().strip(),
                'company_link' : job.css('a.hidden-nested-link::attr(href)').get(),
                'date' : job.css('time::attr(datetime)').get(),
            }
            yield item

            # Log a message for each successful job scraped
            log_message = f"Scraped job - Title: {item['title']}, Company: {item['company']}"
            self.log(log_message)
        
        log_message = f"location: {location}, keyword: {keyword}, page: {page}, url: {response.url}" 
        self.log_to_file(log_message)

        pass

    def clean_link(self, link):
        if link:
            # Split the link by '&' and get the first part
            parts = link.split('&')
            if parts:
                first_part = parts[0]
                # Remove 'ph.' from the first part
                cleaned_link = first_part.replace('ph.', '')
                return cleaned_link
        return None

    def log_to_file(self, message):
        with open('log.txt', 'a') as f:
            f.write(message + '\n')