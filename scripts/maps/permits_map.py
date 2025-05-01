import pandas as pd
import folium
from shapely import wkt
import geopandas as gpd
from pyproj import CRS
from folium import FeatureGroup, Popup

# === Load data ===
df = pd.read_csv('data/processed/properties_with_renovation_flags.csv')
df = df.dropna(subset=['geometry'])
df['geometry'] = df['geometry'].apply(wkt.loads)

# === Load lead scores ===
lead_df = pd.read_csv('data/processed/top_gc_leads.csv')
lead_bins = set(lead_df['BIN'].astype(str))

# === Filter to Brooklyn + sample ===
df = df[df['Borough'].isin(['BK', 'MN'])].sample(n=150000, random_state=42)

# === Convert to GeoDataFrame ===
gdf = gpd.GeoDataFrame(df, geometry='geometry')
gdf.crs = CRS('EPSG:2263')
gdf = gdf.to_crs('EPSG:4326')

# === Group permits per BIN (latest 3) ===
permit_cols = ['job_type', 'permit_status', 'issuance_date']
gdf['BIN'] = gdf['BIN'].astype(str)
grouped = df.dropna(subset=['job_type']).copy()
grouped['BIN'] = grouped['BIN'].astype(str)
latest_permits = grouped.groupby('BIN').apply(
    lambda x: x.sort_values('issuance_date', ascending=False).head(3)
).reset_index(drop=True)

# === Create lookup HTML block for permit display ===
bin_permit_html = {}
for bin_id, permits in latest_permits.groupby('BIN'):
    html = ""
    for _, row in permits.iterrows():
        html += (
            f"<b>{row['job_type']}</b> – {row['permit_status']} ({row['issuance_date'][:10]})<br>"
        )
    bin_permit_html[bin_id] = html

# === Create Folium map ===
m = folium.Map(location=[40.6782, -73.9442], zoom_start=12, tiles="cartodbpositron")

# === Feature groups ===
off_market = FeatureGroup(name='Off-Market Candidates', show=True)
renovated = FeatureGroup(name='Recently Renovated', show=True)
gc_leads = FeatureGroup(name='Top GC Leads', show=True)
other = FeatureGroup(name='Other Properties', show=False)

# === Add polygons with popups ===
for _, row in gdf.iterrows():
    color = "#999999"  # default gray
    group = other
    bin_id = str(row.get("BIN"))

    if bin_id in lead_bins:
        color = "#f4a261"  # orange for GC leads
        group = gc_leads
    elif row.get("off_market_candidate"):
        color = "#e63946"  # red
        group = off_market
    elif row.get("renovation_after_sale"):
        color = "#2a9d8f"  # green
        group = renovated

    popup_html = f"""
    <b>Address:</b> {row.get('Address', 'N/A')}<br>
    <b>Sale Price:</b> ${row.get('SALE PRICE', 'N/A')}<br>
    <b>Sale Date:</b> {row.get('SALE DATE', 'N/A')}<br>
    <b>Zone:</b> {row.get('ZoneDist1', 'N/A')}<br>
    <b>Neighborhood:</b> {row.get('NEIGHBORHOOD', 'N/A')}<br>
    <b>Lot Area:</b> {row.get('LotArea', 'N/A')}<br>
    <b>Building Area:</b> {row.get('BldgArea', 'N/A')}<br>
    <b>Units (Residential):</b> {row.get('UnitsRes', 'N/A')}<br>
    <b>Units (Total):</b> {row.get('UnitsTotal', 'N/A')}<br>
    <b>Year Built:</b> {row.get('YearBuilt', 'N/A')}<br>
    <b>BIN:</b> {bin_id}<br>
    """

    if bin_id in bin_permit_html:
        popup_html += f"<br><b>Recent Permits:</b><br>{bin_permit_html[bin_id]}"

    polygon = folium.GeoJson(
        row.geometry.__geo_interface__,
        style_function=lambda x, c=color: {
            "fillColor": c,
            "color": "gray",
            "weight": 1,
            "fillOpacity": 0.5
        }
    )
    popup = Popup(folium.IFrame(popup_html, width=300, height=250), max_width=300)
    polygon.add_child(popup)
    group.add_child(polygon)

# === Add layers to map ===
off_market.add_to(m)
renovated.add_to(m)
gc_leads.add_to(m)
other.add_to(m)
folium.LayerControl().add_to(m)

# === Save map ===
output_file = 'outputs/html/nyc_lots_bk_with_renovation_flags.html'
m.save(output_file)
print(f"✅ Renovation map with permits, GC leads, and insight popups saved to {output_file}")
