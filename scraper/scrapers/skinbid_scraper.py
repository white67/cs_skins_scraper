import requests
from scrapers.base_scraper import BaseScraper
from models.model_skinbid import SkinBidParser
from config import SKINBID_HEADERS, SKINBID_MARKETPLACE, SKINBID_LIMIT, SKINBID_API_URL, SKINBID_JSON_KEYWORD

class SkinBidScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            parser=SkinBidParser,
            marketplace_name=SKINBID_MARKETPLACE,
            cache_size=SKINBID_LIMIT
        )
        self.base_url = SKINBID_API_URL
        self.headers = SKINBID_HEADERS

    def fetch_raw_data(self) -> list[dict]:
        try:
            response = self.session.get(
                self.base_url,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json().get(SKINBID_JSON_KEYWORD, [])
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            return []