import csv
import random
import time
import logging
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
import pandas as pd
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Set up logging
logging.basicConfig(filename='scraping.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Constants
desired_language = 'en-US'
#BASE_DIR = 'C:\\Users\\aky\\AppData\\Local\\Programs\\Python\\Python38\\course-u\\src\\linkedin_scrapy\\'
BASE_DIR = 'C:\\Users\\aky\\AppData\\Local\\Programs\\Python\\Python38\\course_test\\course-u\\course_u\\src\\linkedin_scrapy'
csv_input_link = BASE_DIR + '\\selenium\\jobs_clean_4.csv'
csv_output = BASE_DIR + '\\selenium\\jobs_post_4.csv'
max_requests = 150
target_count = 125 # len of jobs_clean_4.csv 
max_retries = 2
save_to_csv = True
max_element_wait = 1
min_rest = 60 # 1 minutes
max_rest = 120 # 3 minutes


success_count = 0
skipped_count = 0
need_login_count = 0
has_missing_data_count = 0
timeout_error_count = 0
exception_error_count = 0
finished_count = 0
total_count = 0

# Keyword ID mapping
keyword_id_mapping = {
    "software development": 1,
    "data and analytics": 2,
    "design and ui/ux": 3,
    "product management": 4,
    "testing and quality assurance": 5,
    "security": 6
}


# User agents
user_agents = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; rv:85.0) Gecko/20100101 Firefox/85.0",
]

# Create Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--lang={}'.format(desired_language))
driver_path = BASE_DIR + '\\selenium\\chromedriver.exe'
service = webdriver.ChromeService(executable_path=driver_path)
scraped_urls = set()

# Function to get a random user agent
def get_random_user_agent():
    return random.choice(user_agents)

# Function to clean the link
def clean_link(link):
    if link:
        parts = link.split('&')
        if parts:
            first_part = parts[0]
            return first_part.replace('ph.', '')
    return None

# Function to get text from an element
def get_text(xpath):
    try:
        return WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath))).text
        #return driver.find_element(By.XPATH, xpath).text
    except:
        return None

def show_report(message, display=True, log=False):
    if display:
        print(message)
    if log:
        logging.info(message)


# Function to extract job data
def extract_job_data(job, keyword):
    return {
        'link': clean_link(job.css('a.base-card__full-link ::attr(href)').get()),
        'keyword': keyword,
        'title': job.css('h3::text').get().strip(),
        'company': job.css('a.hidden-nested-link::text').get().strip(),
        'company_link': job.css('a.hidden-nested-link::attr(href)').get(),
        'date_posted': job.css('time::attr(datetime)').get(),
    }

# Define a threshold for the number of scraped URLs before introducing a sleep
sleep_threshold = 50  # Adjust this value as needed

# Main scraping function
def scrape_jobs(url, row, driver):
    global success_count 
    global skipped_count 
    global need_login_count 
    global has_missing_data_count 
    global timeout_error_count 
    global exception_error_count 
    global finished_count
    global total_count
    global df

    retry_count = 0

    while retry_count < max_retries:
        url = row['link']
        total_count += 1
        
        show_report(f"{success_count} ({finished_count}) out of {target_count} URLs scraped, from {total_count} URLs")
        show_report(f"Trying to scrape Job Title: {row['title']} from Company: {row['company']}")
        show_report(f"On Retry {retry_count + 1} out of {max_retries + 1}")
        #url = clean_link(url)

        if url not in scraped_urls:
            try:
                driver.get(url)
                isLogin = get_text("//h1")
                if isLogin == 'Join LinkedIn':
                    show_report("Sign in required. Skipping this URL...")
                    skipped_count += 1
                    need_login_count += 1
                    retry_count = max_retries
                    continue

                Job_Title = get_text("//h1")
                Location = get_text("//span[@class='topcard__flavor topcard__flavor--bullet']")
                Seniority_Level = get_text("(//span[@class='description__job-criteria-text description__job-criteria-text--criteria'])[1]")
                Employment_Type = get_text("(//span[@class='description__job-criteria-text description__job-criteria-text--criteria'])[2]")
                Job_Function = get_text("(//span[@class='description__job-criteria-text description__job-criteria-text--criteria'])[3]")
                Industries = get_text("(//span[@class='description__job-criteria-text description__job-criteria-text--criteria'])[4]")

                driver.find_element(By.XPATH, "//button[@aria-label='Show more, visually expands previously read content above']").click()
                Job_Description = driver.find_element(By.XPATH, "//div[@class='show-more-less-html__markup relative overflow-hidden']").get_attribute('innerHTML')

                if None in (Job_Title, Location, Employment_Type, Job_Function, Industries, Seniority_Level):
                    show_report("One or more data points are missing. Skipping this URL...")
                    skipped_count += 1
                    retry_count = max_retries
                    has_missing_data_count += 1
                    for data in (Job_Title, Location, Employment_Type, Job_Function, Industries, Seniority_Level):
                            if data is None:
                                show_report(f"{data} is missing")
                    continue
                else:
                    show_report("Scraping successful!")
                # print('id:', success_count + 1)
                # print('Llink:', url)
                # print('job_title:', Job_Title)
                # print('company_name:', row['company'])
                # print('company_link:', clean_link(row['company_link']))
                # print('date_link:', row['date'])
                # print('keyword:', row['keyword'])
                # print('keyword_id:', keyword_id_mapping[row['keyword']])
                # print('location:', Location)
                # print('seniority_level:', Seniority_Level)
                # print('employment_type:', Employment_Type)
                # print('job_function:', Job_Function)
                # print('industries:', Industries)
                # print('job_description len:', len(Job_Description))

                data = {
                    'id': success_count + 1,
                    'link': url,
                    'job_title': Job_Title,
                    'company_name': row['company'],
                    'company_link': clean_link(row['company_link']),
                    'date_posted': row['date'],
                    'keyword': row['keyword'],
                    'keyword_id': keyword_id_mapping[row['keyword']],
                    'location': Location,
                    'seniority_level': Seniority_Level,
                    'employment_type': Employment_Type,
                    'job_function': Job_Function,
                    'industries': Industries,
                    'job_description': Job_Description
                }
                show_report(f"Appending data to dataframe...{data}")
                #df = df.append(data, ignore_index=True)
                # concat
                df = pd.concat([df, pd.DataFrame(data, index=[0])], ignore_index=True)
                success_count += 1

                show_report(f"Job Title: { Job_Title}")
                show_report(f"Company Name: {row['company']}")
                show_report(f"Date: {row['date']}")
                show_report(f"Keyword: {row['keyword']}")
                show_report(f"Location: {Location}")
                show_report(f"Employment Type: {Employment_Type}")
                show_report(f"Job Function: {Job_Function}")
                show_report(f"Industries: {Industries}")
                show_report(f"Seniority Level: {Seniority_Level}")

                show_report(f"Job Description: {Job_Description[:15]}...")
                show_report("-" * 50)

            except TimeoutException:
                retry_count += 1
                timeout_error_count += 1
                show_report(f"TimeoutException scraping {url}")
            except Exception as e:
                retry_count += 1
                exception_error_count += 1
                show_report(f"Error scraping {url}: {str(e)}" )
        
        else:
            show_report("URL already scraped. Skipping...")
            retry_count = max_retries
            continue

        scraped_urls.add(url)
        finished_count += 1
        time.sleep(random.randint(1, 3)) # Sleep for 1-5 seconds

        if total_count == target_count:
            show_report("Target count reached. Exiting...")
            break
        



# Initialize the web driver (make sure the driver executable is in your PATH)
#executable_path = BASE_DIR + 'selenium\\chromedriver.exe'
#driver = webdriver.Chrome(options=options, executable_path=executable_path)
driver = webdriver.Chrome(service=service, options=options)
#print("Driver Locaction",driver.service.executable_path)

# Main loop
with open(csv_input_link, 'r', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)

    df = pd.DataFrame(columns=['id', 'link', 'job_title', 'company_name', 'company_link', 'date_posted',
                               'keyword', 'keyword_id', 'location', 'employment_type', 'job_function',
                               'industries', 'seniority_level', 'job_description'])

    driver = webdriver.Chrome(service=service, options=options)
    for row in csvreader:
        if finished_count >= target_count:
            show_report("Target count reached. Exiting...")
            break

        show_report("Inside for loop")
        # Introduce a sleep if the threshold is reached
        if total_count != 0 and total_count % sleep_threshold == 0:
            sleep_duration = random.randint(min_rest, max_rest)  # Sleep for 3-5 minutes
            show_report(f"Reached the sleep threshold. Sleeping for {sleep_duration} seconds...")
            time.sleep(sleep_duration)
            selected_user_agent = get_random_user_agent()
            options.add_argument(f"user-agent={selected_user_agent}")
            show_report("Switching User agent: %s", selected_user_agent)
            driver = webdriver.Chrome(service=service, options=options)

        show_report(f"Scraping URL: {row['link']}")
        scrape_jobs(row['link'], row, driver)

    driver.quit()

    if save_to_csv:
        show_report("Saving to CSV...")
        df.to_csv(csv_output, index=False, encoding='utf-8')
        show_report("Successfully saved to CSV!")

    print(f"Total URLs: {total_count} out of {target_count}")
    print(f"Scraped URLs: {success_count} out of {target_count}")
    print(f"Skipped URLs: {skipped_count} out of {target_count}")
    print(f"Need Login URLs: {need_login_count} out of {skipped_count} skipped")
    print(f"Missing Data URLs: {has_missing_data_count} out of {skipped_count} skipped")
    print(f"Timeout Errors: {timeout_error_count} out of {target_count}")
    print(f"Exception Errors: {exception_error_count} out of {target_count}")
    print(f"Finished URLs: {finished_count} out of {target_count}")
    print("Done!")