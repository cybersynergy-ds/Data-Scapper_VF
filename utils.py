
import os
from bs4 import BeautifulSoup

def extract_job_data_from_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')


        h2_tag = soup.find('h2', class_='p1N2lc')
        job_name = h2_tag.get_text(strip=True) if h2_tag else "Unknown"


        company_span = soup.find('span', class_='RP7SMd')
        company_name = company_span.find('span').get_text(strip=True) if company_span and company_span.find('span') else "Unknown"


        job_location = "Unknown"
        place_icon = soup.find('i', string='place')
        if place_icon:
            sibling = place_icon.find_next_sibling('span', class_='r0wTof')
            if sibling:
                job_location = sibling.get_text(strip=True)


        level_span = soup.find('span', class_='wVSTAb')
        entry_level = level_span.get_text(strip=True) if level_span else "Unknown"


        description_div = soup.find('div', class_='aG5W3')
        if description_div:
            h3 = description_div.find('h3')
            if h3:
                h3.decompose()
            job_description = description_div.get_text(separator=' ', strip=True)
        else:
            job_description = "Unknown"


        responsibilities = []
        resp_div = soup.find('div', class_='bE3reb')
        if resp_div:
            paragraphs = resp_div.find_all('p', class_='ciFk0')
            responsibilities = [p.get_text(strip=True) for p in paragraphs]

        minimum_qualifications = []
        preferred_qualifications = []

        for header in soup.find_all('h3'):
            header_text = header.get_text(strip=True).lower()
            ul = header.find_next_sibling('ul')
            if ul:
                items = [li.get_text(strip=True) for li in ul.find_all('li')]
                if 'minimum' in header_text:
                    minimum_qualifications.extend(items)
                elif 'preferred' in header_text:
                    preferred_qualifications.extend(items)

        # === Job ID from filename ===
        job_id = os.path.basename(file_path).replace('.html', '').replace('job_', '')

        job_data = {
            "job_id": job_id,
            "job_title": job_name,
            "company_name": company_name,
            "job_location": job_location,
            "entry_level": entry_level,
            "minimum_qualifications": minimum_qualifications,
            "preferred_qualifications": preferred_qualifications,
            "job_description": job_description,
            "responsibilities": responsibilities
        }

        return job_data

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

