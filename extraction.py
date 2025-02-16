import time
import save  # Import the save module
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

def scrape_jobs(email, password, job_type, delay_time):
    job_data = []  # List to store extracted job data

    # Selenium WebDriver setup
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    service = Service("chromedriver")  # Ensure chromedriver is in your folder
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open LinkedIn and log in
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)

        driver.find_element(By.ID, "username").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(delay_time)

        # Search for jobs
        driver.get("https://www.linkedin.com/jobs")
        time.sleep(2)
        search_box = driver.find_element(By.XPATH, "//input[contains(@placeholder,'Search jobs')]")
        search_box.send_keys(job_type)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        # Extract job details
        job_cards = driver.find_elements(By.CLASS_NAME, "job-card-container")[:10]  # Adjust as needed

        for job in job_cards:
            try:
                ActionChains(driver).move_to_element(job).click().perform()
                time.sleep(2)

                # Extract job details
                title = driver.find_element(By.CLASS_NAME, "topcard__title").text
                company = driver.find_element(By.CLASS_NAME, "topcard__org-name-link").text
                location = driver.find_element(By.CLASS_NAME, "topcard__flavor").text
                description = driver.find_element(By.CLASS_NAME, "description__text").text
                job_link = driver.current_url

                # Extract job posting date
                try:
                    posted_on = driver.find_element(By.CLASS_NAME, "posted-time-ago__text").text
                except:
                    posted_on = "N/A"

                # Extract company LinkedIn profile link
                try:
                    company_link = driver.find_element(By.CLASS_NAME, "topcard__org-name-link").get_attribute("href")
                except:
                    company_link = "N/A"

                # Extract HR details (if available)
                try:
                    hr_name = driver.find_element(By.CLASS_NAME, "hirer__name").text
                    hr_link = driver.find_element(By.CLASS_NAME, "hirer__name a").get_attribute("href")
                except:
                    hr_name = "N/A"
                    hr_link = "N/A"

                # Store job details
                job_data.append({
                    "Job Title": title,
                    "Posted On": posted_on,
                    "Job Description": description,
                    "Job Link": job_link,
                    "Company Name": company,
                    "Company LinkedIn": company_link,
                    "HR Name": hr_name,
                    "HR LinkedIn": hr_link
                })

            except Exception as e:
                print(f"Skipping job due to error: {e}")

        driver.quit()

        # Pass data to save.py for storage
        save.save_to_excel(job_data)

    except Exception as e:
        driver.quit()
        print(f"Error in extraction: {e}")

