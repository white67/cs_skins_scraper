import requests
import time
import json
import logging
import os
import random

from scraper.config import CACHE_FILE, LOGS_FILE, BACKEND_API_URL
from scraper.models.model_csfloat import ListingCSFLOAT
from scraper.scrapers.base_scraper import BaseScraper
from scraper.config import CSFLOAT_API_URL, CSFLOAT_HEADERS, CSFLOAT_MARKETPLACE, CSFLOAT_SCRAPE_INTERVAL, CSFLOAT_LIMIT

class CSFLOATScraper(BaseScraper):
    """
    Scraper for CSFLOAT marketplace.
    """
    def __init__(self):
        super().__init__(marketplace_name=CSFLOAT_MARKETPLACE, api_url=CSFLOAT_API_URL)
        self.headers = CSFLOAT_HEADERS
        self.scrape_interval = CSFLOAT_SCRAPE_INTERVAL
        self.api_limit = CSFLOAT_LIMIT

    def scrape(self, cache_listings: list[dict]):
        """
        Scrape new listings from CSFLOAT marketplace.
        """
        
        raw_data = self.fetch_data(endpoint="", headers=self.headers)
        
        raw_data = raw_data["data"]
        if not raw_data:
            return []
        else:
            new_listings = []
            for listing in raw_data:
                listing_dict = ListingCSFLOAT(listing).map_to_base().to_dict()
                if listing_dict not in cache_listings:
                    new_listings.append(listing_dict)

        return new_listings, cache_listings
    
    ####### REUSABLE FUNCTIONS #######
    
    def setup_logger(marketplace_name):
        """
        Setup logger for the scraper.
        """
        log_file = LOGS_FILE + f"{marketplace_name}.log"
        logger = logging.getLogger(marketplace_name)
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        if not logger.handlers:
            logger.addHandler(handler)
        
        return logger

    def load_cache(marketplace_name):
        """
        Load cached listings from a file.
        """
        filename = CACHE_FILE + f"{marketplace_name}_cache.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
        return []

    def save_cache(cache_listings, marketplace_name):
        """
        Save cache to a file.
        """
        filename = CACHE_FILE + f"{marketplace_name}_cache.json"
        with open(filename, "w") as f:
            json.dump(cache_listings, f, indent=4)
            
    def get_randomized_interval(base_interval, variation=0.2):
        """
        Returns a randomized interval within ±variation% of the base interval.
        """
        factor = 1 + random.uniform(-variation, variation)
        randomized_interval = base_interval * factor
        return max(1, randomized_interval)  # Ensure it's never below 1 second

    def run_scraper(SCRAPER):
        """
        Scrape and send new listings to API.
        """
        
        logger = CSFLOATScraper.setup_logger(SCRAPER.marketplace_name)
        cache_listings = CSFLOATScraper.load_cache(SCRAPER.marketplace_name)
        
        while True:
            try:
                print(f"cache_listings: {len(cache_listings)}")
                new_listings, cache_listings = SCRAPER.scrape(cache_listings)
                
                if new_listings:
                    # Send to API
                    response = requests.post(BACKEND_API_URL, json=new_listings)
                    if response.status_code == 201:
                        logger.info(f"Found new listing batch ({len(new_listings)} items)")
                    else:
                        logger.error(f"API Error: {response.status_code} - {response.text}")

                # Maintain cache size
                cache_listings.extend(new_listings)
                cache_listings = cache_listings[-SCRAPER.api_limit:]

                # Save cache to file
                CSFLOATScraper.save_cache(cache_listings, SCRAPER.marketplace_name)
                
            except Exception as e:
                logger.error(f"Error in fetch_new_listings: {str(e)}")
            
            interval = CSFLOATScraper.get_randomized_interval(SCRAPER.scrape_interval)
            logger.info(f"Sleeping for {interval:.2f} seconds")
            
            time.sleep(interval)