import requests
from scrapers.base_scraper import BaseScraper
from models.model_csfloat import CSFloatParser
from config import CSFLOAT_MARKETPLACE, CSFLOAT_HEADERS, CSFLOAT_API_URL, CSFLOAT_LIMIT, CSFLOAT_JSON_KEYWORD

class CSFloatScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            parser=CSFloatParser,
            marketplace_name=CSFLOAT_MARKETPLACE,
            cache_size=CSFLOAT_LIMIT
        )
        self.base_url = CSFLOAT_API_URL
        self.headers = CSFLOAT_HEADERS

    def fetch_raw_data(self) -> list[dict]:
        try:
            response = self.session.get(
                self.base_url,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json().get(CSFLOAT_JSON_KEYWORD, [])
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            return []