# clear the webdriver cache if the code does not work
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import re
import json
from utils import extract_job_data_from_html


base_url = "https://www.google.com/about/careers/applications/jobs/results?q=%22Data+Engineer%22&sort_by=date"
job_base_url = "https://www.google.com/about/careers/applications/"
output_folder = "backup_htmls"
output_json = "job_details.json"

options = Options()
options.add_argument("--headless=new") 
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

os.makedirs(output_folder, exist_ok=True)

driver.get(base_url)
time.sleep(2) 

job_links = driver.find_elements(By.CSS_SELECTOR, 'a.VfPpkd-mRLv6.VfPpkd-RLmnJb')

job_hrefs = []
for a in job_links:
    href = a.get_attribute("href")
    if href and "jobs/results/" in href:
        full_url = href if href.startswith("http") else job_base_url + href
        job_hrefs.append(full_url)

print(f"Found {len(job_hrefs)} job links.")

all_jobs = []


if os.path.exists(output_json):
    with open(output_json, "r", encoding="utf-8") as jf:
        try:
            all_jobs = json.load(jf)
        except json.JSONDecodeError:
            all_jobs = []

for i, job_url in enumerate(job_hrefs):
    try:
        driver.get(job_url)
        time.sleep(2) 
        html = driver.page_source
        
        job_path = job_url.split("/")[-1].split("?")[0]
        safe_job_id = re.sub(r'[<>:"/\\|?*]', '', job_path)
        
        filename = f"job_{i+1}.html"
        filepath = os.path.join(output_folder, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        job_data = extract_job_data_from_html(filepath)
        
 
        if os.path.exists(filepath):
            os.remove(filepath)

        if job_data:
            all_jobs.append(job_data)

        print(f"Saved and processed job {i+1}: {filename} (HTML deleted)")

    except Exception as e:
        print(f"Error with job {i+1}: {e}")

driver.quit()


with open(output_json, "w", encoding="utf-8") as jf:
    json.dump(all_jobs, jf, indent=2, ensure_ascii=False)

print(f"Saved all job data to {output_json}")
