import json
from db_connection import get_connection
from mysql.connector import Error

def insert_job(job):
    insert_sql = """
    INSERT INTO jobs_info (
        job_id,
        job_title,
        company_name,
        job_location,
        entry_level,
        minimum_qualifications,
        preferred_qualifications,
        job_description,
        responsibilities
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(insert_sql, (
            job["job_id"],
            job["job_title"],
            job["company_name"],
            job["job_location"],
            job["entry_level"],
            json.dumps(job.get("minimum_qualifications", [])),
            json.dumps(job.get("preferred_qualifications", [])),
            job["job_description"],
            json.dumps(job.get("responsibilities", [])),
        ))

        conn.commit()
        print(f"Inserted job ID: {job['job_id']}")

    except Error as e:
        if "1062" in str(e):
            print(f"Duplicate job skipped: {job['job_title']} at {job['company_name']} in {job['job_location']}")
        else:
            print(f"Error inserting job {job['job_id']}: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def load_and_insert_jobs(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        jobs = json.load(f)
    
    for job in jobs:
        if job.get("h1b_sponsorship") is True:
            insert_job(job)

if __name__ == "__main__":
    load_and_insert_jobs("filtered_job_details.json")
