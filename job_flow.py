# pip install "prefect>=2.14,<3.0.0"
# prefect deployment build job_flow.py:job_flow --name "Hourly Job Scraper" --interval 3600
# prefect deployment apply job_flow-deployment.yaml
# prefect agent start

from prefect import flow, task
import subprocess

@task
def scrape_jobs():
    subprocess.run(["python", "main.py"], check=True)

@task
def filter_jobs():
    subprocess.run(["python", "data_filtering.py"], check=True)

@task
def insert_jobs_to_db():
    subprocess.run(["python", "populate_db.py"], check=True)

@flow(name="Job Scraper and Loader")
def job_flow():
    scrape_jobs()
    filter_jobs()
    insert_jobs_to_db()

if __name__ == "__main__":
    job_flow()
