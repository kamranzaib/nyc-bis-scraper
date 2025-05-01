import requests
import pandas as pd
import time
from pathlib import Path

# === Setup ===
BASE_URL = "https://data.cityofnewyork.us/resource/ipu4-2q9a.json"
LIMIT = 50000
OFFSET = 0
BOROUGH = "BROOKLYN"
OUTPUT_FILE = Path("data/raw/permits/construction_jobs_brooklyn.csv")

# Create folder if needed
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# === Fields to extract ===
FIELDS = [
    "bin__", "job__", "job_doc__", "job_type", "self_cert", "block", "lot", "borough",
    "house__", "street_name", "zip_code", "bldg_type", "work_type", "permit_status",
    "filing_status", "permit_type", "permit_sequence__", "permit_subtype",
    "filing_date", "issuance_date", "expiration_date", "job_start_date",
    "permittee_s_first_name", "permittee_s_last_name", "permittee_s_business_name",
    "permittee_s_license_type", "permittee_s_license__",
    "owner_s_business_type", "owner_s_business_name",
    "owner_s_first_name", "owner_s_last_name", "owner_s_phone__",
    "dobrundate", "estimated_job_cost"
]

# === Pull data in 50k batches ===
all_records = []
print("Starting fetch for borough: BROOKLYN")

while True:
    params = {
        "$limit": LIMIT,
        "$offset": OFFSET,
        "$where": f"borough='{BOROUGH}'",
        "$select": ",".join(FIELDS)
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f"Failed batch at offset {OFFSET}: {response.status_code}")
        break

    batch = response.json()
    if not batch:
        print("No more records.")
        break

    all_records.extend(batch)
    print(f"Fetched {len(batch)} records (offset {OFFSET})")
    OFFSET += LIMIT
    time.sleep(1)  # avoid rate limits

# === Save to CSV ===
df = pd.DataFrame(all_records)
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Saved {len(df)} records to {OUTPUT_FILE}")
