import pandas as pd

# === Load Rolling Sales XLSX ===
sales_df = pd.read_excel("/Users/kamranxeb/Downloads/rollingsales_brooklyn.xlsx", skiprows=4)

# Clean & build BBL
sales_df['BOROUGH'] = sales_df['BOROUGH'].astype(str)
sales_df['BLOCK'] = sales_df['BLOCK'].astype(str).str.zfill(5)
sales_df['LOT'] = sales_df['LOT'].astype(str).str.zfill(4)
sales_df['BBL'] = sales_df['BOROUGH'] + sales_df['BLOCK'] + sales_df['LOT']

# Filter meaningful sales
sales_df = sales_df[sales_df['SALE PRICE'] > 10000]
sales_df['SALE DATE'] = pd.to_datetime(sales_df['SALE DATE'], errors='coerce')

# === Load your properties + permits data ===
props_df = pd.read_csv("properties_with_permits.csv")
props_df['BBL'] = props_df['BBL'].astype(str)

# === Merge sales into property dataset ===
merged_df = props_df.merge(
    sales_df[['BBL', 'SALE DATE', 'SALE PRICE', 'NEIGHBORHOOD', 'BUILDING CLASS AT TIME OF SALE']],
    on='BBL',
    how='left'
)

# === Save merged output ===
merged_df.to_csv("properties_with_sales.csv", index=False)
print("✅ Saved properties_with_sales.csv")
