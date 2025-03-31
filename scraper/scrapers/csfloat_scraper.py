# csfloat scrape logic to scrape data from marketplaces based on base_scraper.py
from scraper.models.model_csfloat import ListingCSFLOAT
from scraper.scrapers.base_scraper import BaseScraper
from scraper.config import CSFLOAT_API_URL, CSFLOAT_HEADERS, CSFLOAT_MARKETPLACE

class CSFLOATScraper(BaseScraper):
    """
    Scraper for CSFLOAT marketplace.
    """
    def __init__(self):
        super().__init__(marketplace_name=CSFLOAT_MARKETPLACE, api_url=CSFLOAT_API_URL)

    def scrape(self, cache_listings: list[dict]):
        raw_data = self.fetch_data(endpoint="", headers=CSFLOAT_HEADERS)
        
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