import json
import csv
import re

def normalize_name(name):
    """Lowercase and remove punctuation for loose comparison."""
    return re.sub(r'[^a-z0-9]', '', name.lower())


h1b_normalized_names = set()

with open("h1bcompanies_list.csv", "r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None) 
    for row in reader:
        if row:
            h1b_normalized_names.add(normalize_name(row[0]))


with open("job_details.json", "r", encoding="utf-8") as f:
    job_data = json.load(f)


for job in job_data:
    raw_name = job.get("company_name", "")
    normalized = normalize_name(raw_name)
    

    job["h1b_sponsorship"] = any(
        h1b_name in normalized or normalized in h1b_name
        for h1b_name in h1b_normalized_names
    )


with open("filtered_job_details.json", "w", encoding="utf-8") as f:
    json.dump(job_data, f, indent=2, ensure_ascii=False)

print("Done: Saved to filtered_job_details.json")
