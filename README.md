# NYC BIS Scraper

A web scraper for the NYC Building Information System (BIS) using Playwright.

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install Playwright browsers:
   ```
   playwright install
   ```

## Usage

Run the scraper:
```
python scraper.py
```

This will scrape information for the example BIN numbers included in the script and save the results to `nyc_property_data.csv`.

## Customization

Edit the `bin_numbers` list in `scraper.py` to include the Building Identification Numbers (BINs) you want to scrape.

## Notes

- The script includes random delays between requests to avoid being blocked
- Adjust the CSS selectors in the script if the website structure changes
- The script uses Playwright with headless browser to handle JavaScript-rendered content
```
nyc-bis-scraper
├─ README.md
├─ __init__.py
├─ config.py
├─ data
│  ├─ __init__.py
│  ├─ api_data
│  │  ├─ __init__.py
│  │  └─ bin_to_bbl_mapping.csv
│  ├─ final_properties.csv
│  ├─ processed
│  │  ├─ __init__.py
│  │  ├─ bin_bbl_essential_data.csv
│  │  ├─ bin_bbl_with_pluto_data.csv
│  │  ├─ final_properties.csv
│  │  ├─ permits_last5yrs.csv
│  │  ├─ properties_with_permits.csv
│  │  ├─ properties_with_renovation_flags.csv
│  │  ├─ properties_with_sales.csv
│  │  └─ top_gc_leads.csv
│  ├─ properties_master.csv
│  ├─ properties_with_permits.csv
│  ├─ properties_with_sales.csv
│  └─ raw
│     ├─ __init__.py
│     ├─ bin_bbl_links
│     │  ├─ __init__.py
│     │  ├─ bin_to_bbl_mapping.csv
│     │  └─ pluto_bbls.csv
│     ├─ permits
│     │  ├─ __init__.py
│     │  ├─ construction_jobs_brooklyn.csv
│     │  └─ dob_permits_since_2020.jsonl
│     ├─ pluto
│     │  ├─ MapPLUTO.cpg
│     │  ├─ MapPLUTO.dbf
│     │  ├─ MapPLUTO.prj
│     │  ├─ MapPLUTO.sbn
│     │  ├─ MapPLUTO.sbx
│     │  ├─ MapPLUTO.shp
│     │  ├─ MapPLUTO.shx
│     │  └─ __init__.py
│     └─ quotes
│        ├─ __init__.py
│        └─ reference_job_costs.csv
├─ debug_pluto.py
├─ docker
│  ├─ __init__.py
│  └─ docker-compose.yml
├─ final_properties.csv
├─ nyc_bis_scraper
│  ├─ __init__.py
│  ├─ run.py
│  └─ scripts
│     ├─ __init__.py
│     ├─ analysis
│     │  ├─ __init__.py
│     │  ├─ analyze_renovation_stats.py
│     │  └─ score.py
│     ├─ extractors
│     │  ├─ __init__.py
│     │  ├─ construction_webscraper.py
│     │  ├─ fetch_construction_jobs.py
│     │  ├─ footprints.py
│     │  ├─ permits.py
│     │  ├─ pluto.py
│     │  └─ sales.py
│     ├─ maps
│     │  ├─ Property_map.py
│     │  ├─ __init__.py
│     │  ├─ map.py
│     │  ├─ map_generator.py
│     │  └─ permits_map.py
│     ├─ mergers
│     │  ├─ __init__.py
│     │  ├─ build_master.py
│     │  └─ property_data_merger.py
│     ├─ pipeline
│     │  ├─ __init__.py
│     │  ├─ config.yaml
│     │  └─ run_pipeline.py
│     └─ test_postgis_connection.py
├─ nyc_emergency_work_map.html
├─ nyc_property_map_enhanced.html
├─ nycscraper
├─ outputs
│  ├─ __init__.py
│  ├─ html
│  │  ├─ __init__.py
│  │  ├─ days_to_permit_histogram.png
│  │  ├─ nyc_emergency_work_map.html
│  │  ├─ nyc_lots_bk_fixed.html
│  │  ├─ nyc_lots_bk_with_permit_layers.html
│  │  ├─ nyc_lots_bk_with_permits.html
│  │  ├─ nyc_lots_bk_with_renovation_flags.html
│  │  ├─ nyc_lots_map.html
│  │  ├─ nyc_property_map.html
│  │  └─ property_polygon_map.html
│  ├─ logs
│  │  └─ __init__.py
│  └─ properties_master_test.csv
├─ properties_with_permits.csv
├─ requirements.txt
├─ restructure.py
├─ setup.py
├─ test_import.py
└─ tests
   ├─ __init__.py
   ├─ test_build_master.py
   ├─ test_build_master_simple.py
   ├─ test_footprints.py
   ├─ test_imports.py
   └─ test_script.py

```