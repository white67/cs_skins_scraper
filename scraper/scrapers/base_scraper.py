import os
import time
import random
import requests
import psycopg2

import json
import logging
from scraper.config import CACHE_FILE, LOGS_FILE, BACKEND_API_URL
from scraper.models.base_model import Listing

class BaseScraper:
    """
    Base class for scrapers.
    """
    def __init__(self, marketplace_name: str, api_url: str, ListingMODEL=None, headers=None, scrape_interval=60, api_limit=50, json_keyword=None):
        self.marketplace_name = marketplace_name
        self.api_url = api_url
        self.ListingMODEL = ListingMODEL
        self.headers = headers
        self.scrape_interval = scrape_interval
        self.api_limit = api_limit
        self.json_keyword = json_keyword
        self.consecutive_errors = 0
        
    def scrape(self, cache_listings: list[dict]):
        """
        Scrape new listings from XXX marketplace.
        """
        
        raw_data = self.fetch_data(endpoint="", headers=self.headers)
        
        raw_data = raw_data[self.json_keyword]
        if not raw_data:
            return []
        else:
            new_listings = []
            for listing in raw_data:
                listing_dict = self.ListingMODEL(listing).map_to_base().to_dict()
                if listing_dict not in cache_listings:
                    new_listings.append(listing_dict)
        return new_listings, cache_listings

    def run_scraper(self):
        """
        Scrape and send new listings to API.
        """
        
        logger = self.setup_logger()
        cache_listings = self.load_cache()
        
        while True:
            try:
                new_listings, cache_listings = self.scrape(cache_listings)
                
                if new_listings:
                    # Send to API
                    response = requests.post(BACKEND_API_URL, json=new_listings)
                    if response.status_code == 201:
                        logger.info(f"Found new listing batch ({len(new_listings)} items)")
                    else:
                        logger.error(f"API Error: {response.status_code} - {response.text}")

                # Maintain cache size
                cache_listings.extend(new_listings)
                cache_listings = cache_listings[-self.api_limit:]

                # Save cache to file
                self.save_cache(cache_listings)
                
                self.consecutive_errors = 0
                interval = self.get_randomized_interval()
                
            except Exception as e:
                logger.error(f"Error in fetch_new_listings: {str(e)}")
                self.consecutive_errors += 1
                interval = min(40 * self.consecutive_errors, 300)
            
            logger.info(f"Sleeping for {interval:.2f} seconds")
            time.sleep(interval)

    def fetch_data(self, endpoint, headers={}):
        """
        Fetch data from the API endpoint.
        """
        
        url = f"{self.api_url}{endpoint}"
        print(f"Fetching data from {url}")
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    
    def sleep_random(self):
        """
        Sleep for a random time between 8 and 12 seconds.
        """
        time.sleep(random.uniform(8, 12))
    
    def insert_listing_to_db(self, listing: Listing):
        """
        Inserts a single listing into the PostgreSQL database.
        """
        
        try:
            # Load environment variables
            DB_HOST = os.getenv("DB_HOST")
            DB_PORT = os.getenv("DB_PORT")
            DB_NAME = os.getenv("DB_NAME")
            DB_USER = os.getenv("POSTGRES_USER")
            DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
            
            # Connect to PostgreSQL database
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            cursor = conn.cursor()

            # Prepare the insert query
            insert_query = listing.generate_insert_query()
            
            # Prepare the data to insert
            data = listing.to_db_tuple()
            
            # Execute the query
            cursor.execute(insert_query, data)

            # Commit the transaction
            conn.commit()

            print(f"Inserted listing {listing.item_name} into database.")

        except Exception as e:
            print(f"Error inserting listing to database: {e}")
        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()

    def insert_new_listings_to_db(self, new_listings):
        """
        Inserts a list of new listings into the database.
        """
        for listing in new_listings:
            self.insert_listing_to_db(listing)
    
    ####### REUSABLE SCRAPERS FUNCTIONS #######

    def setup_logger(self):
        """
        Setup logger for the scraper.
        """
        log_file = LOGS_FILE + f"{self.marketplace_name}.log"
        logger = logging.getLogger(self.marketplace_name)
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        if not logger.handlers:
            logger.addHandler(handler)
        
        return logger

    def load_cache(self):
        """
        Load cached listings from a file.
        """
        filename = CACHE_FILE + f"{self.marketplace_name}_cache.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
        return []

    def save_cache(self, cache_listings):
        """
        Save cache to a file.
        """
        filename = CACHE_FILE + f"{self.marketplace_name}_cache.json"
        with open(filename, "w") as f:
            json.dump(cache_listings, f, indent=4)
            
    def get_randomized_interval(self, variation=0.2):
        """Returns interval between 5s and scrape_interval (±20%)"""
        base = self.scrape_interval
        randomized = base * (1 + random.uniform(-variation, variation))
        return max(1, randomized)