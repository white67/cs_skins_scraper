# csfloat scrape logic to scrape data from marketplaces based on base_scraper.py
from scraper.models.model_skinport import ListingSKINPORT
from scraper.scrapers.base_scraper import BaseScraper
from scraper.config import SKINPORT_API_URL, SKINPORT_HEADERS, SKINPORT_MARKETPLACE

class CSFLOATScraper(BaseScraper):
    """
    Scraper for SKINPORT marketplace.
    """
    def __init__(self):
        super().__init__(marketplace_name=SKINPORT_MARKETPLACE, api_url=SKINPORT_API_URL)

    def scrape(self, cache_listings: list[dict]):
        raw_data = self.fetch_data(endpoint="", headers=SKINPORT_HEADERS)
        
        raw_data = raw_data["items"]
        if not raw_data:
            return []
        else:
            new_listings = []
            for listing in raw_data:
                listing_dict = ListingSKINPORT(listing).map_to_base().to_dict()
                if listing_dict not in cache_listings:
                    new_listings.append(listing_dict)

        return new_listings, cache_listings