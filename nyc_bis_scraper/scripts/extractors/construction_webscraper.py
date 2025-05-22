import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# === Output ===
output_file = Path("data/raw/quotes/reference_job_costs.csv")
output_file.parent.mkdir(parents=True, exist_ok=True)

# === Scrape Thumbtack home building cost guide ===
url = "https://www.thumbtack.com/p/home-building-cost-by-sqft"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}

logger.info(f"Requesting URL: {url}")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

records = []

# Function to extract dollar amounts from text
def extract_dollar_amount(text):
    match = re.search(r'\$[\d,]+(?:\.\d+)?', text)
    if match:
        return match.group(0)
    return None

# Find all elements with the specific class
cost_elements = soup.find_all(class_="Type_title3___voqu")
logger.info(f"Found {len(cost_elements)} elements with the target class")

# Only process the first 20 elements
cost_elements = cost_elements[:20]
logger.info(f"Processing the first 20 elements")

# Find all flex columns with costs (for the additional costs)
flex_columns = soup.find_all('ul', class_=lambda c: c and 'flex-column' in c and 'stack_root' in c)
additional_costs = []

# Process flex column costs
logger.info("Processing flex column costs...")
for flex_col in flex_columns:
    list_items = flex_col.find_all('li')
    for item in list_items:
        # Find text and cost within list item
        spans = item.find_all('span')
        p_elements = item.find_all('p')
        
        cost_text = ""
        description = ""
        
        # Extract from spans 
        for span in spans:
            span_text = span.get_text(strip=True)
            if '$' in span_text:
                cost_text = span_text
            elif len(span_text) > 5:  # Likely a description
                description += span_text + " "
                
        # Extract from p elements
        for p in p_elements:
            p_text = p.get_text(strip=True)
            if '$' in p_text:
                cost_text = p_text
            elif len(p_text) > 5:  # Likely a description
                description += p_text + " "
                
        if cost_text and '$' in cost_text:
            cost = extract_dollar_amount(cost_text)
            additional_costs.append({
                "source": "thumbtack-guide",
                "job_type": description.strip() if description else "Additional Cost",
                "quote_text": cost_text,
                "extracted_cost": cost
            })
            logger.info(f"Added additional cost: {description} - {cost}")

# Process each main cost element
for i, element in enumerate(cost_elements, 1):
    # Get element ID and text
    element_id = element.get('id', f"Unknown-{i}")
    element_text = element.get_text(strip=True)
    
    logger.info(f"Processing element {i}: ID={element_id}, Text={element_text}")
    
    cost_found = False
    
    # Strategy 1: Find the closest parent div
    parent_div = element.parent
    
    # Find the next div.mb4 after this element's parent
    next_div = parent_div.find_next_sibling('div', class_='mb4')
    
    # Find the cost span inside this div (with class="b")
    if next_div:
        cost_span = next_div.find('span', class_='b')
        if cost_span and '$' in cost_span.text:
            cost_text = cost_span.get_text(strip=True)
            
            records.append({
                "source": "thumbtack-guide",
                "item_number": i,
                "job_type": element_text,
                "quote_text": cost_text,
                "extracted_cost": cost_text
            })
            
            logger.info(f"Added: {element_text} - {cost_text}")
            cost_found = True
    
    # Strategy 2: Look for paragraphs after the heading
    if not cost_found:
        next_p = element.find_next('p')
        if next_p and '$' in next_p.get_text():
            cost_text = next_p.get_text(strip=True)
            cost = extract_dollar_amount(cost_text)
            
            records.append({
                "source": "thumbtack-guide",
                "item_number": i,
                "job_type": element_text,
                "quote_text": cost_text,
                "extracted_cost": cost
            })
            
            logger.info(f"Added (from paragraph): {element_text} - {cost}")
            cost_found = True
    
    # Strategy 3: Look for cost info in a broader area
    if not cost_found:
        # Look for all price elements in the vicinity
        next_elements = []
        current = element.next_sibling
        for _ in range(10):  # Look at next 10 elements
            if current:
                if hasattr(current, 'get_text'):
                    text = current.get_text(strip=True)
                    if '$' in text:
                        next_elements.append(current)
                current = current.next_sibling if hasattr(current, 'next_sibling') else None
            else:
                break
        
        if next_elements:
            cost_text = next_elements[0].get_text(strip=True)
            cost = extract_dollar_amount(cost_text)
            
            records.append({
                "source": "thumbtack-guide",
                "item_number": i,
                "job_type": element_text,
                "quote_text": cost_text,
                "extracted_cost": cost
            })
            
            logger.info(f"Added (broader search): {element_text} - {cost}")
            cost_found = True
    
    # Strategy 4: Look for specific phrases in text
    if not cost_found:
        # Get key terms from the element text
        key_terms = element_text.lower().replace(str(i) + ".", "").split()
        
        # Find paragraphs containing both a key term and a dollar sign
        dollar_paragraphs = soup.find_all(['p', 'span'], string=lambda s: s and '$' in s)
        for p in dollar_paragraphs:
            p_text = p.get_text(strip=True).lower()
            if any(term in p_text for term in key_terms if len(term) > 3):
                cost_text = p.get_text(strip=True)
                cost = extract_dollar_amount(cost_text)
                
                records.append({
                    "source": "thumbtack-guide",
                    "item_number": i,
                    "job_type": element_text,
                    "quote_text": cost_text,
                    "extracted_cost": cost
                })
                
                logger.info(f"Added (keyword match): {element_text} - {cost}")
                cost_found = True
                break
    
    if not cost_found:
        logger.warning(f"No cost information found for {element_text}")

# Combine main costs and additional costs
all_records = records + additional_costs

# === Save extracted cost info ===
if all_records:
    df = pd.DataFrame(all_records)
    df.to_csv(output_file, index=False)
    logger.info(f"✅ Extracted {len(df)} cost categories from Thumbtack guide and saved to {output_file}")
    
    # Show summary
    main_count = len(records)
    additional_count = len(additional_costs)
    logger.info(f"Main costs: {main_count}, Additional costs: {additional_count}")
else:
    logger.error("No cost information was found on the page.")