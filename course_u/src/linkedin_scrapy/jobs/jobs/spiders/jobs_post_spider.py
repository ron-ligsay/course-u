import scrapy
import pandas as pd
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
import logging
from scrapy_splash import SplashRequest


class JobsPostSpiderSpider(scrapy.Spider):
    name = "jobs_post_spider"
    allowed_domains = ["linkedin.com"]
    #start_urls = ['https://www.linkedin.com/']#["https://ph.linkedin.com/jobs/view/"]
    #start_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?'
    #start_url = 'https://ph.linkedin.com/jobs/search?'
    #start_url = 'https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs'
    start_url = 'https://ph.linkedin.com/jobs/search?keywords=&location=&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
    custom_settings = {
        #'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'REDIRECT_ENABLED': False,
    }
     # Define a dictionary to map keywords to IDs
    keyword_id_mapping = {
        "software development": 1,
        "data and analytics": 2,
        "design and ui/ux": 3,
        "testing and quality assurance": 4,
        "networking and infrastructure": 5
    }



    def __init__(self, csv_file, *args, **kwargs):
        super(JobsPostSpiderSpider, self).__init__(*args, **kwargs)
        start_url = 'https://ph.linkedin.com/jobs/search?keywords=&location=&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
        self.logger = logging.getLogger(__name__)
        self.csv_file = csv_file
        self.df = pd.read_csv(self.csv_file)
        self.url = list(self.df['link'])
        self.keyword = list(self.df['keyword'])
        self.date = list(self.df['date'])
        self.company_link = list(self.df['company_link'])

    def start_requests(self):
        for url, keyword, date, company_link in zip(self.url, self.keyword, self.date, self.company_link):
            script = """
                function main(splash, args)
                    splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
                    splash:go(args.url)
                    splash:wait(2)  -- Adjust the waiting time as needed
                    return {
                        url = splash:url(),
                        html = splash:html(),
                    }
                end
                """
            # yield scrapy.Request(
            #     url=url, 
            #     callback=self.parse, 
            #     meta={'keyword': keyword, 'date': date},#, 'dont_redirect': True
            #     dont_filter=True, # import to avoid filtering out the request
            #     endpoint='execute',
            #     args={
            #         'lua_source': script,
            #         #'timeout': 90,
            #     },
            #     errback=self.error_handler
            # )
            yield SplashRequest(
                url=url,
                callback=self.parse,
                endpoint='execute',
                args={
                    'lua_source': script,
                    'wait': 5,  # Adjust the waiting time as needed
                },
                meta={
                    'keyword': keyword,
                    'date': date,
                    # You can add other meta information as needed
                },
                dont_filter=True,  # Import to avoid filtering out the request
                errback=self.error_handler
            )


    def parse(self, response):
        self.logger.info("This is a log message from the parse method.")
        self.logger.info(f"Scraping page: {response.url}")
        try:
            # check if the response status code is 200 (OK)
            if response.status != 200:
                self.logger.error(f"Skipping URL {response.url} due to non-200 status code ({response.status})")
                print(f"Skipping URL {response.url} due to non-200 status code ({response.status})")
                return # Skip this URL

            url = response.url
            title = response.css('h1::text').get(default='nan').strip()
            keyword = response.meta['keyword']
            date = response.meta['date']
            company = response.css('a.topcard__org-name-link::text').get(default='nan').strip()
            company_link = response.css('a.topcard__org-name-link::attr(href)').get(default='nan')
            location = response.css('span.topcard__flavor--bullet::text').get(default='nan').strip()
            description = response.css('div.description__text ::text').getall(default='nan')
            description = ''.join(description).strip()
            seniority = response.css('span.description__job-criteria-text::text')[0].get(default='nan').strip()
            job_function = response.css('span.description__job-criteria-text::text')[1].get(default='nan').strip()
            employment_type = response.css('span.description__job-criteria-text::text')[2].get(default='nan').strip()
            industries = response.css('span.description__job-criteria-text::text')[3].get(default='nan').strip()
            application_link = response.css('a.sign-up-modal__company_webiste::attr(href)').get(default='nan')

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
            print(f"Error in parsing - {response.url}")

        pass

    def error_handler(self, failure):
        # Handle errors and generate a report here
        if failure.check(HttpError):
            response = failure.value.response
            if response.status == 404:
                self.logger.error(f"404 Error: Page not found - {response.url}")
                # Generate a report or take other actions as needed
        elif failure.check(DNSLookupError, TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error(f"Request timed out - {request.url}")
            # Generate a report or take other actions as needed