import pandas as pd

# === Step 1: Load permits JSONL ===
permits = pd.read_json("dob_permits_since_2020.jsonl", lines=True)

# === Step 2: Filter for valid issuance_date since 2020-04-23 ===
permits["issuance_date"] = pd.to_datetime(permits["issuance_date"], errors="coerce")
permits = permits[permits["issuance_date"] >= "2020-04-23"]

# === Step 3: Load property dataset ===
properties = pd.read_csv("final_properties.csv")  # This should have BIN as a column

# === Step 4: Join permits to properties using BIN ===
merged = properties.merge(
    permits,
    how="left",
    left_on="BIN",   # From your parcels dataset
    right_on="bin__",  # From the DOB permits
)

# === Step 5: Save final merged dataset ===
merged.to_csv("properties_with_permits.csv", index=False)

print(f"✅ Merged dataset saved with {len(merged)} rows.")
