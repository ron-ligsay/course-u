

### Notes
https://www.youtube.com/watch?v=hCARQVJy_mk


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

ctrl+d to exit shell

py -m pip install -U prompt-toolkit

.get(default="")