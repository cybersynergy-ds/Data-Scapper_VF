# Job Scraper and Loader

video solution : https://drive.google.com/file/d/10zmOykph5EGZJ9M08YqMMybE95Vhe5Lz/view?usp=sharing

## Overview  
This project automates scraping job listings from a Google Jobs website, filters the data, and loads it into a MySQL database. It also supports automated periodic every hour runs to fetch only new job entries and avoid duplication.

---

## Approach

### Step 1: Scraping Job Data  
- Utilized Selenium WebDriver with ChromeDriver to scrape jobs from the target site.  
- Configured headless Chrome for efficient and silent scraping.

### Step 2: Data Filtering and Cleaning  
- Parsed the scraped JSON data to filter jobs where `h1b_sponsorship` is `true`.  
- Transformed and cleaned data to match database schema requirements and create              filtered_job_details json.

### Step 3: Database Setup and Insertion  
- Designed MySQL table `jobs_info` with all the important and appropriate columns and JSON fields for complex attributes.  
- Implemented connection handling through a dedicated module reading credentials securely from environment variables and automatically eastablishing connection.  
- Added uniqueness checks on job title, company name, and location to prevent duplicate inserts.

### Step 4: Automation  
- Scheduled scraping and data loading every hour using Prefect.  
- Workflow configured to only insert new job listings by checking for existing entries.

---
## Setup Instructions

### Prerequisites  
- Python 3.12+  
- MySQL Server (running locally or accessible remotely)  
- Google Chrome browser installed  
- Required Python packages (install with `pip install -r requirements.txt`) for installing required packages.

### Environment Variables  
Create a `.env` file in the project root with the following content:  
```env
DB_HOST=localhost
DB_USER=user_name (that will be set by the user)
DB_PASSWORD=your_password (set by user during installation)
DB_NAME=job_details_db (database created by user to store all relevant tables)
```
### Running Locally
1. Initialize databse schema by running create_table.py
2. Run the main.py for starting the data scrapping using selenium which will be stored in job_details.json
3. Then run the data_filtering.py, it will filter the important jobs with H1B sponsored companies.
4. populate the db with the filtered values using populate_db.py.
5. Automation is handles by Prefect for hourly capture of data and also makes sure no only unique data is sent to database, so we run the job_flow.py.

### Challenges and Solutions
- ChromeDriver version mismatch:
Resolved by using webdriver-manager to automatically download the compatible ChromeDriver version.
- Web Scrapping: Utilized BeautifulSoup to efficiently parse and extract relevant data from HTML content, focusing on key job attributes such as company name, job title, location, and other essential fields.
- Environment variable management:
Used python-dotenv to load sensitive DB credentials from a .env file instead of hardcoding for not exposing personal details.
- Data duplication prevention:
Added a technique of adding an extra boolean column (True/False) in the json, so during db insertion directly check that parameter and send only the unique data to job_detail_db.
- Automation with Prefect:
Faced version command changes in Prefect CLI it was only working for version between 2.14 and <=3 ; resolved by referring to updated official docs and testing with desgining minimal flows before scheduling.
- Handling JSON data in MySQL:
Stored complex fields as JSON strings and ensured proper serialization/deserialization during insert and retrieval.
