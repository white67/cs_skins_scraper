# csfloat scrape logic to scrape data from marketplaces based on base_scraper.py
from models.marketplace_csfloat import ListingCSFLOAT
from scrapers.base_scraper import BaseScraper
from config import CSFLOAT_API_URL
from config import CSFLOAT_HEADERS

class CSFLOATScraper(BaseScraper):
    """
    Scraper for CSFLOAT marketplace.
    """
    def __init__(self):
        super().__init__(marketplace_name="CSFLOAT", api_url=CSFLOAT_API_URL)

    def scrape(self):
        raw_data = self.fetch_data(endpoint="", headers=CSFLOAT_HEADERS)
        # print(f"Raw data: {type(raw_data)}")
        
        raw_data = raw_data["data"]
        if not raw_data:
            return []
        
        new_listings = []
        for listing in raw_data:
            new_listing = ListingCSFLOAT(listing).map_to_base()
            new_listings.append(new_listing)
        
        self.insert_new_listings_to_db(new_listings)

        return new_listings