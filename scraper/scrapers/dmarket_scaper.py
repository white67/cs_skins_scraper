from scraper.models.model_dmarket import ListingDMARKET
from scraper.scrapers.base_scraper import BaseScraper
from scraper.config import DMARKET_API_URL, DMARKET_MARKETPLACE, DMARKET_SCRAPE_INTERVAL, DMARKET_LIMIT, DMARKET_JSON_KEYWORD
from scraper.utils import *

class DMARKETScraper(BaseScraper):
    """
    Scraper for DMARKET marketplace.
    """
    def __init__(self):
        super().__init__(
            marketplace_name=DMARKET_MARKETPLACE, 
            api_url=DMARKET_API_URL, 
            ListingMODEL=ListingDMARKET,
            scrape_interval=DMARKET_SCRAPE_INTERVAL, 
            api_limit=DMARKET_LIMIT,
            json_keyword=DMARKET_JSON_KEYWORD
        )