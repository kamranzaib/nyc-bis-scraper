import pandas as pd

# === Load the processed data ===
df = pd.read_csv("data/processed/properties_with_renovation_flags.csv")

# === Convert columns ===
df["SALE PRICE"] = pd.to_numeric(df["SALE PRICE"], errors="coerce")
df["ZoneDist1"] = df["ZoneDist1"].astype(str)

# === Define a simple lead score ===
df["lead_score"] = (
    (df["off_market_candidate"] == True).astype(int) * 2 +
    (df["SALE PRICE"] > 1_000_000).astype(int) +
    (df["ZoneDist1"].str.startswith("R")).astype(int)
)

# === Sort by score and recent sale date ===
df_sorted = df.sort_values(by=["lead_score", "SALE DATE"], ascending=[False, False])

# === Save top leads to CSV ===
top_leads = df_sorted[df_sorted["lead_score"] >= 2].copy()
top_leads.to_csv("data/processed/top_gc_leads.csv", index=False)
print("✅ Top GC leads saved to data/processed/top_gc_leads.csv")
