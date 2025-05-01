import requests
import json
import time

BASE_URL = "https://data.cityofnewyork.us/resource/ipu4-2q9a.json"
START_DATE = "2020-04-23"
LIMIT = 50000
MAX_PAGES = 20  # Adjust as needed
OUTPUT_FILE = "dob_permits_since_2020.jsonl"

with open(OUTPUT_FILE, "w") as f:
    for i in range(MAX_PAGES):
        offset = i * LIMIT
        params = {
            "$limit": LIMIT,
            "$offset": offset
        }
        print(f"Fetching permits {offset}–{offset+LIMIT}...")
        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            break

        data = response.json()
        if not data:
            print("No more data.")
            break

        for row in data:
            f.write(json.dumps(row) + "\n")

        time.sleep(1)  # Respectful delay between requests

print(f"Saved permits to {OUTPUT_FILE}")
