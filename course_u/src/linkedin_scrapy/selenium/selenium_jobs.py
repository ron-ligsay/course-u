import csv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
import time
import pandas as pd
import logging
import random


# Proxy Ratation



# set up logging
logging.basicConfig(filename='scraping.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Set the desired language
desired_language = 'en-US'

# user agent
#user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
user_agents = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; rv:85.0) Gecko/20100101 Firefox/85.0",
]

# Randomize user agent
select_user_agent = random.choice(user_agents)
# Function to get a random user agent
def get_random_user_agent():
    return random.choice(user_agents)


# Create Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--lang={}'.format(desired_language))
options.add_argument(f'user-agent={select_user_agent}')

# Initialize the web driver (make sure the driver executable is in your PATH)
driver = webdriver.Chrome(chrome_options=options) #,executable_path=driver_path


BASE_DIR = 'C:\\Users\\aky\\AppData\\Local\\Programs\\Python\\Python38\\course-u\\src\\linkedin_scrapy\\selenium\\'
csv_input_link = BASE_DIR + 'jobs1.csv'
csv_output = BASE_DIR + 'jobs_post.csv'

# Define a set to store scraped URLs
scraped_urls = set()

target_count = 100
total_count = 0
success_count = 0
skipped_count = 0
need_login_count = 0
has_missing_data_count = 0
finished_count = 0

save_to_csv = True

 # Define a dictionary to map keywords to IDs
keyword_id_mapping = {
    "software development": 1,
    "data and analytics": 2,
    "design and ui/ux": 3,
    "testing and quality assurance": 4,
    "networking and infrastructure": 5
}


# get text by xpath
def get_text(xpath):
    try:
        return WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath))).text
        #return driver.find_element(By.XPATH, xpath).text
    except:
        return None

display = True
log = False

def show_report(message, data=None):
    if display:
        print(message, data)
    if log:
        logging.info(message, data)

# Create the CSV file and write the header row
fieldnames = ['jobpost_id','Link', 'Job_Title', 'Company_Name', 'Company_link','Date','Keyword','Keyword_id','Location', 'Employment_Type', 'Job_Function', 'Industries', 'Seniority_Level','Job_Description']
df = pd.DataFrame(columns=fieldnames)

# include column in csv_input_link
# columns_to_include = ['link','keyword','title','company','company_link','date']

# Read links from a CSV file (assuming 'links.csv' has a 'url' column)
with open(csv_input_link, 'r', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)

    for row in csvreader:
        url = row['link']
        total_count += 1

        # Set maximum number of retries
        max_retries = 2
        retry_count = 0

        while retry_count < max_retries:
            try:

                # Add a random user agent for each request
                selected_user_agent = get_random_user_agent()
                options.add_argument(f"user-agent={selected_user_agent}")

                # Remove ".ph" from the URL
                cleaned_url = url.replace('ph.', '')

                # Remove unnecessary query parameters
                cleaned_url = cleaned_url.split('?')[0]
                
                # Check if the URL has been scraped before
                if cleaned_url not in scraped_urls:
                    # Display url
                    show_report("Now Scraping Link: ", cleaned_url)
                    print(total_count, " out of ", target_count)
                    print("On retry ", retry_count+1, " out of ", max_retries)
                    # Open the URL in the web driver
                    driver.get(cleaned_url)

                    # Pause for a few seconds after opening the page
                    #time.sleep(30)

                    isLogin = get_text("//h1")
                    if isLogin == 'Join LinkedIn':
                        show_report("Sign in required. Skipping this URL...")
                        skipped_count += 1
                        need_login_count += 1
                        retry_count = max_retries
                        continue
                    
                    Job_Title = get_text("//h1")
                    
                    #Company_Name = get_text("//a[@class='topcard__org-name-link topcard__flavor--black-link']")
                    Location = get_text("//span[@class='topcard__flavor topcard__flavor--bullet']")
                    Seniority_Level = get_text("(//span[@class='description__job-criteria-text description__job-criteria-text--criteria'])[1]")
                    Employment_Type = get_text("(//span[@class='description__job-criteria-text description__job-criteria-text--criteria'])[2]")
                    Job_Function = get_text("(//span[@class='description__job-criteria-text description__job-criteria-text--criteria'])[3]")
                    Industries = get_text("(//span[@class='description__job-criteria-text description__job-criteria-text--criteria'])[4]")
                    
                    
                    # click see more
                    driver.find_element(By.XPATH,"//button[@aria-label='Show more, visually expands previously read content above']").click()
                    # get html content
                    Job_Description = driver.find_element(By.XPATH,"//div[@class='show-more-less-html__markup relative overflow-hidden']").get_attribute('innerHTML')
                    
                    #Company_Description = get_text()
                    #Company_Website = get_text()

                    # Check if any of the scraped data is empty
                    if None in (Job_Title, Location, Employment_Type, Job_Function, Industries, Seniority_Level): #Company_Name, 
                        # Skip this URL
                        show_report("One or more data points are missing. Skipping this URL...")
                        skipped_count += 1
                        retry_count = max_retries
                        # print out the missing data
                        for data in (Job_Title, Location, Employment_Type, Job_Function, Industries, Seniority_Level):
                            if data is None:
                                show_report(data, " is missing")
                        has_missing_data_count += 1
                        continue
                    else:        
                        show_report("Scraping successful!")
                    
                    # Write data to the CSV file
                    #  ['jobpost_id','Link', 'Job_Title', 'Company_Name', 'Company_link','Date','Keyword','Location', 'Employment_Type', 'Job_Function', 'Industries', 'Seniority_Level','Description']
                    if save_to_csv:
                        data = {
                            'jobpost_id': success_count+1,
                            'Link': cleaned_url,
                            'Job_Title': Job_Title,
                            'Company_Name': row['company'],
                            'Company_link': row['company_link'], # 'Company_Link': Company_Link,
                            'Date' : row['date'],
                            'Keyword': row['keyword'], # 'Keyword': Keyword,
                            'Keyword_id': keyword_id_mapping[row['keyword']], # 'Keyword_id': Keyword_id,
                            'Location': Location,
                            'Seniority_Level': Seniority_Level,
                            'Employment_Type': Employment_Type,
                            'Job_Function': Job_Function,
                            'Industries': Industries,
                            
                            'Job_Description': Job_Description
                        }

                        # Append the data to the DataFrame
                        df = df.append(data, ignore_index=True)
                        success_count += 1

                        # Print for Verification
                        #show_report(Job_Title, " from ", Company_Name)
                        show_report("Job Title: ", Job_Title)
                        show_report("Company Name: ", row['company'])
                        show_report("Date: ", row['date'])
                        show_report("Keyword: ", row['keyword'])
                        show_report("Location: ", Location)
                        show_report("Employment Type: ", Employment_Type)
                        show_report("Job Function: ", Job_Function)
                        show_report("Industries: ", Industries)
                        show_report("Seniority Level: ", Seniority_Level)
                        # print html content with tags
                        show_report(Job_Description)
                        #print("Job Description: ", Job_Description)

                        show_report("-"*50)

                else:
                    print("URL already scraped. Skipping...")
                    skipped_count += 1
                    
                # if successful, break out of the loop
                break

            except TimeoutException:
                retry_count += 1
                print(f"TimeoutException scraping {url}")

            except Exception as e:
                print(f"Error scraping {url}: {str(e)}")

        # end of while loop
        finished_count += 1
        time.sleep(random.randint(1, 5))
        # add the URL to the set
        scraped_urls.add(cleaned_url)

        # exit after N link
        if total_count == target_count:
           show_report("Target count reached. Exiting...")
           break
        

# Close the web driver when done
driver.quit()

# Save the DataFrame to a CSV file
if save_to_csv:
    df.to_csv(csv_output, index=False, encoding='utf-8')


# Print some stats
print(f"Total URLs: {total_count} out of {target_count}")
print(f"Scraped URLs: {success_count} out of {target_count}")
print(f"Skipped URLs: {skipped_count} out of {target_count}")
print(f"Need Login URLs: {need_login_count} out of {skipped_count} skipped")
print(f"Missing Data URLs: {has_missing_data_count} out of {skipped_count} skipped")
print(f"Finished URLs: {finished_count} out of {target_count}")
print("Done!")
