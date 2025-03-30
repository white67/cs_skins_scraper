# csfloat scrape logic to scrape data from marketplaces based on base_scraper.py
from models.marketplace_csfloat import ListingCSFLOAT
from scrapers.base_scraper import BaseScraper
from models.base_model import Listing
from config import CSFLOAT_API_URL
from config import CSFLOAT_PARAMS

class CSFLOATScraper(BaseScraper):
    """
    Scraper for CSFLOAT marketplace.
    """
    def __init__(self):
        super().__init__(marketplace_name="CSFLOAT", api_url=CSFLOAT_API_URL)

    def scrape(self):
        raw_data = self.fetch_data(endpoint="", headers=CSFLOAT_PARAMS)
        print(f"Raw data: {type(raw_data)}")
        raw_data = raw_data["data"]
        if not raw_data:
            return []
        
        new_listings = []
        
        for listing in raw_data:
            new_listing = ListingCSFLOAT(listing).map_to_base()
            new_listings.append(new_listing)
        
        return new_listings

        