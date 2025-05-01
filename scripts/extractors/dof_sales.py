import pandas as pd
from pathlib import Path

# === Step 1: Define paths ===
input_path = Path("properties_with_sales.csv")
output_path = Path("data/processed_data/properties_with_renovation_flags.csv")

# === Step 2: Load data ===
print(f"📥 Loading: {input_path}")
df = pd.read_csv(input_path)

# === Step 3: Clean & convert dates ===
df["SALE DATE"] = pd.to_datetime(df["SALE DATE"], errors="coerce")
df["issuance_date"] = pd.to_datetime(df["issuance_date"], errors="coerce")

# === Step 4: Time between sale and permit ===
df["days_to_permit"] = (df["issuance_date"] - df["SALE DATE"]).dt.days

# === Step 5: Flag renovation that occurred within 1 year of sale ===
df["renovation_after_sale"] = df["days_to_permit"].between(0, 365)

# === Step 6: Flag properties sold recently but no permits yet ===
df["off_market_candidate"] = df["issuance_date"].isna() & (df["SALE DATE"] >= "2023-01-01")

# === Step 7: Save output ===
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)
print(f"✅ Saved: {output_path}")
