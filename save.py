import os
import pandas as pd
from datetime import datetime

def save_to_excel(job_data):
    # Define folder structure
    base_folder = "Bot"
    year_folder = datetime.today().strftime('%Y')
    month_folder = datetime.today().strftime('%B')
    day_folder = datetime.today().strftime('%d')

    folder_path = os.path.join(base_folder, year_folder, month_folder, day_folder)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "linkedin_jobs.xlsx")

    df = pd.DataFrame(job_data)

    # Check if file exists and append data while preventing duplicates
    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)
        df = pd.concat([existing_df, df]).drop_duplicates(subset=["Job Link"], keep="first")

    df.to_excel(file_path, index=False)
    print(f"Job details saved in {file_path}")
