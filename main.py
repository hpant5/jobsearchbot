import time
import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Function to toggle password visibility
def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        toggle_btn.config(text="Hide")
    else:
        password_entry.config(show="*")
        toggle_btn.config(text="Show")

# Function to start LinkedIn login automation
def start_bot():
    email = email_entry.get()
    password = password_entry.get()
    job_type = job_entry.get()
    delay_time = delay_slider.get()

    if not email or not password or not job_type:
        status_label.config(text="Please fill all fields!", foreground="red")
        return

    status_label.config(text="Logging in to LinkedIn...", foreground="blue")

    # Selenium WebDriver setup
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    
    service = Service("chromedriver")  # Ensure this is the correct path
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)

        # Enter login credentials
        driver.find_element(By.ID, "username").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(delay_time)  # Wait before searching

        # Search for jobs
        driver.get("https://www.linkedin.com/jobs")
        time.sleep(2)
        search_box = driver.find_element(By.XPATH, "//input[contains(@placeholder,'Search jobs')]")
        search_box.send_keys(job_type)
        search_box.send_keys(Keys.RETURN)

        status_label.config(text="Search completed! Extracting job details...", foreground="green")
        time.sleep(3)

        # Extract job details
        job_cards = driver.find_elements(By.CLASS_NAME, "job-card-container")[:5]  # Limit to 5 jobs
        job_results = []

        for job in job_cards:
            try:
                title = job.find_element(By.CLASS_NAME, "job-card-list__title").text
                company = job.find_element(By.CLASS_NAME, "job-card-container__company-name").text
                location = job.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text
                job_results.append(f"{title} | {company} | {location}")
            except:
                continue

        driver.quit()

        # Display results
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "\n".join(job_results))
        result_text.config(state=tk.DISABLED)

    except Exception as e:
        status_label.config(text=f"Error: {e}", foreground="red")
        driver.quit()

# GUI Setup
root = tk.Tk()
root.title("LinkedIn Job Scraper Bot")
root.geometry("500x500")

# Email Entry
tk.Label(root, text="LinkedIn Email:").pack()
email_entry = tk.Entry(root, width=40)
email_entry.pack()

# Password Entry with Toggle Button
tk.Label(root, text="LinkedIn Password:").pack()
password_frame = tk.Frame(root)
password_entry = tk.Entry(password_frame, width=30, show="*")
password_entry.pack(side=tk.LEFT)
toggle_btn = tk.Button(password_frame, text="Show", command=toggle_password)
toggle_btn.pack(side=tk.RIGHT)
password_frame.pack()

# Job Type Entry
tk.Label(root, text="Job Type (e.g., Data Science Intern):").pack()
job_entry = tk.Entry(root, width=40)
job_entry.pack()

# Delay Slider
tk.Label(root, text="Delay Before Search (seconds):").pack()
delay_slider = tk.Scale(root, from_=1, to=30, orient="horizontal")
delay_slider.set(3)
delay_slider.pack()

# Start Bot Button
start_btn = tk.Button(root, text="Start Bot", command=start_bot)
start_btn.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="")
status_label.pack()

# Result Box
tk.Label(root, text="Job Results:").pack()
result_text = tk.Text(root, height=10, width=50, state=tk.DISABLED)
result_text.pack()

# Run GUI
root.mainloop()
