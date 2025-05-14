from scraper.models.model_csfloat import ListingCSFLOAT
from scraper.scrapers.base_scraper import BaseScraper
from scraper.config import CSFLOAT_API_URL, CSFLOAT_HEADERS, CSFLOAT_MARKETPLACE, CSFLOAT_SCRAPE_INTERVAL, CSFLOAT_LIMIT, CSFLOAT_JSON_KEYWORD

class CSFLOATScraper(BaseScraper):
    """
    Scraper for CSFLOAT marketplace.
    """
    def __init__(self):
        super().__init__(
            marketplace_name=CSFLOAT_MARKETPLACE, 
            api_url=CSFLOAT_API_URL, 
            ListingMODEL=ListingCSFLOAT, 
            headers = CSFLOAT_HEADERS,
            scrape_interval = CSFLOAT_SCRAPE_INTERVAL,
            api_limit = CSFLOAT_LIMIT,
            json_keyword = CSFLOAT_JSON_KEYWORD
        )