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