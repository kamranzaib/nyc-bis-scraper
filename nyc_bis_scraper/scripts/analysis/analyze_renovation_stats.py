import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your full file
df = pd.read_csv("data/processed/properties_with_renovation_flags.csv")

# Ensure correct types
df["days_to_permit"] = pd.to_numeric(df["days_to_permit"], errors="coerce")
df["SALE DATE"] = pd.to_datetime(df["SALE DATE"], errors="coerce")

# Filter for valid values
valid = df[df["days_to_permit"].notna() & (df["days_to_permit"] >= 0)]

# === Summary Stats ===
total_sales = df["SALE DATE"].notna().sum()
sales_with_permits = valid.shape[0]
pct_renovated = df["renovation_after_sale"].sum() / total_sales * 100
median_days = valid["days_to_permit"].median()

print("\n🧠 Renovation Summary:")
print(f"- Total properties sold: {total_sales}")
print(f"- Sales that led to permits: {sales_with_permits}")
print(f"- % Renovated within 1 year: {pct_renovated:.2f}%")
print(f"- Median days to permit: {int(median_days)} days")

# === Histogram Plot ===
plt.figure(figsize=(10, 6))
sns.histplot(valid["days_to_permit"], bins=50, color="#1976d2")
plt.title("Distribution of Days Between Sale and Permit Issuance")
plt.xlabel("Days to Permit")
plt.ylabel("Number of Properties")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/html/days_to_permit_histogram.png")
print("\n📊 Histogram saved to: outputs/html/days_to_permit_histogram.png")
