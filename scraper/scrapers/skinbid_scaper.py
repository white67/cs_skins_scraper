from scraper.config import CACHE_FILE, LOGS_FILE, BACKEND_API_URL
from scraper.models.model_skinbid import ListingSKINBID
from scraper.scrapers.base_scraper import BaseScraper
from scraper.config import SKINBID_API_URL, SKINBID_HEADERS, SKINBID_MARKETPLACE, SKINBID_SCRAPE_INTERVAL, SKINBID_LIMIT, SKINBID_JSON_KEYWORD
from scraper.utils import *

class SKINBIDScraper(BaseScraper):
    """
    Scraper for SKINBID marketplace.
    """
    def __init__(self):
        super().__init__(
            marketplace_name=SKINBID_MARKETPLACE, 
            api_url=SKINBID_API_URL, 
            ListingMODEL=ListingSKINBID, 
            headers=SKINBID_HEADERS, 
            scrape_interval=SKINBID_SCRAPE_INTERVAL, 
            api_limit=SKINBID_LIMIT,
            json_keyword=SKINBID_JSON_KEYWORD
        )