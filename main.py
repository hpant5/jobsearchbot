import tkinter as tk
from tkinter import ttk, messagebox
import extraction  # Calls extraction.py to start job search

# Function to toggle password visibility
def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        toggle_btn.config(text="Hide")
    else:
        password_entry.config(show="*")
        toggle_btn.config(text="Show")

# Function to start job scraping
def start_extraction():
    email = email_entry.get()
    password = password_entry.get()
    job_type = job_entry.get()
    delay_time = delay_slider.get()

    if not email or not password or not job_type:
        status_label.config(text="Please fill all fields!", foreground="red")
        return

    status_label.config(text="Extracting jobs from LinkedIn...", foreground="blue")

    # Call the extraction module
    extracted_data = extraction.scrape_jobs(email, password, job_type, delay_time)

    if extracted_data:
        messagebox.showinfo("Success", "Job data extracted successfully!")
    else:
        messagebox.showerror("Error", "Failed to extract job data.")

# GUI Setup
root = tk.Tk()
root.title("LinkedIn Job Scraper Bot")
root.geometry("500x400")

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
delay_slider = tk.Scale(root, from_=1, to=10, orient="horizontal")
delay_slider.set(3)
delay_slider.pack()

# Start Bot Button
start_btn = tk.Button(root, text="Start Extraction", command=start_extraction)
start_btn.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="")
status_label.pack()

# Run GUI
root.mainloop()
