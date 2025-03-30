# base scrape logic to scrape data from marketplaces
import os
import time
import json
import random
import requests

class BaseScraper:
    """
    Base class for scrapers.
    """
    def __init__(self, marketplace_name: str, api_url: str):
        self.marketplace_name = marketplace_name
        self.api_url = api_url

    def fetch_data(self, endpoint, headers={}):
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
        time.sleep(random.uniform(8, 12))