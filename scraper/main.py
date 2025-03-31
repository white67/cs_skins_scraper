import requests
import time
import json
import logging
import os
import random

from scraper.scrapers.csfloat_scraper import CSFLOATScraper
from scraper.config import API_URL, CSFLOAT_LIMIT, CSFLOAT_SCRAPE_INTERVAL

# Logging setup
logging.basicConfig(
    filename="scraper/logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

CACHE_FILE = "scraper/data/cache.json"

def load_cache():
    """Load cached listings from a file."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return []

def save_cache(cache_listings):
    """Save cache to a file."""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_listings, f, indent=4)
        
def get_randomized_interval(base_interval, variation=0.1):
    """Returns a randomized interval within ±variation% of the base interval."""
    factor = 1 + random.uniform(-variation, variation)
    randomized_interval = base_interval * factor
    return max(1, randomized_interval)  # Ensure it's never below 1 second

def fetch_new_listings(cache_listings):
    """Scrape and send new listings to API."""
    try:
        new_listings, cache_listings = CSFLOATScraper().scrape(cache_listings)

        if new_listings:
            # Send to API
            response = requests.post(API_URL, json=new_listings)
            if response.status_code == 201:
                logging.info(f"Found new listing batch ({len(new_listings)} items)")
            else:
                logging.error(f"API Error: {response.status_code} - {response.text}")

        # Maintain cache size
        cache_listings.extend(new_listings)
        cache_listings = cache_listings[-CSFLOAT_LIMIT:]

        # Save cache to file
        save_cache(cache_listings)

        return cache_listings

    except Exception as e:
        logging.error(f"Error in fetch_new_listings: {str(e)}")
        return cache_listings

if __name__ == "__main__":
    cache_listings = load_cache()

    while True:
        cache_listings = fetch_new_listings(cache_listings)
        interval = get_randomized_interval(CSFLOAT_SCRAPE_INTERVAL)
        logging.info(f"Sleeping for {interval:.2f} seconds")
        time.sleep(interval)