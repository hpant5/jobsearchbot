import time
import os
import save  # Calls save.py to store extracted jobs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def scrape_jobs(email, password, job_type, delay_time):
    job_data = []

    # Initialize Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")  # For Linux

    # Use WebDriver Manager to auto-download ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open LinkedIn login page
        driver.get("https://www.linkedin.com/login")
        time.sleep(3)  # Give time for the page to load

        # Enter Email
        email_input = driver.find_element(By.ID, "username")
        email_input.clear()
        email_input.send_keys(email)
        time.sleep(1)

        # Enter Password
        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys(password)
        time.sleep(1)

        # Click Sign In Button
        sign_in_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        sign_in_button.click()

        print("Login successful, waiting for LinkedIn to load...")
        time.sleep(5)  # Wait for LinkedIn to load after login

        # Navigate to Jobs page
        driver.get("https://www.linkedin.com/jobs")
        time.sleep(2)

        # Search for the job type
        search_box = driver.find_element(By.XPATH, "//input[contains(@placeholder,'Search jobs')]")
        search_box.send_keys(job_type)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        # Extract job details
        job_cards = driver.find_elements(By.CLASS_NAME, "job-card-container")[:10]  # Adjust as needed

        for job in job_cards:
            try:
                job.click()
                time.sleep(2)

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
        save.save_to_excel(job_data)
        return job_data  # Return data to `main.py`

    except Exception as e:
        print(f"Error in extraction: {e}")
        driver.quit()
        return None  # Return None in case of failure
