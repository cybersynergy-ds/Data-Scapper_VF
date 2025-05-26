from db_connection import get_connection

def create_jobs_table():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS jobs_info (
        job_id VARCHAR(50) PRIMARY KEY,
        job_title VARCHAR(255) NOT NULL,
        company_name VARCHAR(255),
        job_location VARCHAR(255),
        entry_level VARCHAR(50),
        minimum_qualifications JSON,
        preferred_qualifications JSON,
        job_description TEXT,
        responsibilities JSON
    );
    """

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        print("Table 'jobs_info' created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_jobs_table()
