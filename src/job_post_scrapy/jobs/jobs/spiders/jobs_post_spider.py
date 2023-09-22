import scrapy
import pandas as pd

class JobsPostSpiderSpider(scrapy.Spider):
    name = "jobs_post_spider"
    allowed_domains = ["linkedin.com"]
    #start_urls = ['https://www.linkedin.com/']#["https://ph.linkedin.com/jobs/view/"]

    custom_settings = {
        #'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'REDIRECT_ENABLED': False,
    }

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.df = pd.read_csv(self.csv_file)
        self.url = list(self.df['link_clean'])
        self.keyword = list(self.df['keyword'])
        self.date = list(self.df['date'])

    def start_requests(self):
        for url, keyword, date, company_link in zip(self.url, self.keyword, self.date, self.company_link):
            yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword, 'date': date})

    def parse(self, response):
        try:
            url = response.url
            title = response.css('h1::text').get().strip()
            keyword = response.meta['keyword']
            date = response.meta['date']
            company = response.css('a.topcard__org-name-link::text').get().strip()
            company_link = response.css('a.topcard__org-name-link::attr(href)').get()
            location = response.css('span.topcard__flavor--bullet::text').get().strip()
            description = response.css('div.description__text ::text').getall()
            description = ''.join(description).strip()
            seniority = response.css('span.description__job-criteria-text::text')[0].get().strip()
            job_function = response.css('span.description__job-criteria-text::text')[1].get().strip()
            employment_type = response.css('span.description__job-criteria-text::text')[2].get().strip()
            industries = response.css('span.description__job-criteria-text::text')[3].get().strip()
            application_link = response.css('a.sign-up-modal__company_webiste::attr(href)').get()

            yield {
                'url' : url,
                'title' : title,
                'keyword' : keyword,
                'date' : date,
                'company' : company,
                'company_link' : company_link,
                'location' : location,
                'description' : description,
                'seniority' : seniority,
                'job_function' : job_function,
                'employment_type' : employment_type,
                'industries' : industries,
                'application_link' : application_link
            }

        except:
            print("Error in parsing")

        pass
