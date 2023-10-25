

### Notes
https://www.youtube.com/watch?v=hCARQVJy_mk

https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs

scrapy startproject <project_name>

scrapy shell "<url_link>"

https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?

https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=python&location=Philippines

response.css

li or job post card
job-search-card

jobs = response.css('div.job-search-card')

Job post link
a.base-card__full-link ::atr(href)

Job title
h3

Company name
a.hidden-nested-link::text

Company link
a.hidden-nested-link::attr(href)

Date
time::attr(datetime)


creating a spider
scrapy genspider jobs_spider linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?

running spider
scrapy crawl jobs_spider

scrapy crawl jobs_spider -o jobs.csv


notes:

ctrl+d to exit shell

py -m pip install -U prompt-toolkit

.get(default="")




job posting spider - tags

title
response.css('h1::text').get()

company name
response.css('a.topcard__org-name-link::text').get().strip()

company link
response.css('a.topcard__org-name-link::attr(href)').get()

address
response.css('span.topcard__flavor--bullet::text').get().strip()

description
response.css('div.show-more-less-html__markup').getall()

Seniority Level
response.css('span.description__job-criteria-text::text')[1].get().strip()

Job Function
response.css('span.description__job-criteria-text::text')[2].get().strip()

Employment Type
response.css('span.description__job-criteria-text::text')[3].get().strip()

Industries
response.css('span.description__job-criteria-text::text')[4].get().strip()

apply linkl
response.css('a.sign-up-modal__company_webiste::attr(href)').get()


scrapy crawl job_post_spider -a csv_file=jobs_clean.csv -o job_post.csv



https://ph.linkedin.com/jobs/view/qa-qc-engineer-at-filinvest-development-corporation-3667997744?refId=UEMuM06FHziMghHVtdtg2w%3D%3D&trackingId=F4JIGpUjPPOusBoMKh9S0g%3D%3D
&position=1
&pageNum=0
&trk=public_jobs_jserp-result_search-card