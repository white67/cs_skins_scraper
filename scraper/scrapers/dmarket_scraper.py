import requests
from scrapers.base_scraper import BaseScraper
from models.model_dmarket import DMarketParser
from config import DMARKET_MARKETPLACE, DMARKET_API_URL, DMARKET_LIMIT, DMARKET_JSON_KEYWORD

class DMarketScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            parser=DMarketParser,
            marketplace_name=DMARKET_MARKETPLACE,
            cache_size=DMARKET_LIMIT
        )
        self.base_url = DMARKET_API_URL

    def fetch_raw_data(self) -> list[dict]:
        try:
            response = self.session.get(
                self.base_url
            )
            response.raise_for_status()
            return response.json().get(DMARKET_JSON_KEYWORD, [])
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            return []