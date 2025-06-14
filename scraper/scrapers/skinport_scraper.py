# skinport_scraper.py
import logging
import requests
from pathlib import Path
from skinport import Client
from models.model_skinport import SkinportParser
from config import BACKEND_API_URL, SKINPORT_MARKETPLACE, SKINPORT_JSON_KEYWORD, LOGS_FILE

class SkinportScraper:
    def __init__(self):
        self.marketplace_name = SKINPORT_MARKETPLACE
        self.parser = SkinportParser
        self.client = Client()
        self.logger = self._setup_logger()
        self._register_handlers()

    def _setup_logger(self) -> logging.Logger:
        """Configure marketplace-specific logger"""
        log_dir = Path(LOGS_FILE)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        handler = logging.FileHandler(log_dir / f"{self.marketplace_name}.log")
        handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        ))

        logger = logging.getLogger(self.marketplace_name)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            logger.addHandler(handler)
            
        return logger

    def _register_handlers(self):
        """Register WebSocket event handlers"""
        @self.client.listen("saleFeed")
        async def on_sale_feed(data):
            await self._process_sales(data.get(SKINPORT_JSON_KEYWORD, []))

    async def _process_sales(self, raw_sales: list):
        """Process incoming sales data immediately"""
        try:
            for sale in raw_sales:
                listing = self.parser.parse(sale)
                self._send_to_api([listing])
        except Exception as e:
            self.logger.error(f"Processing error: {str(e)}")

    def _send_to_api(self, listings: list):
        """Send listings to backend API"""
        try:
            response = requests.post(
                BACKEND_API_URL,
                json=[item.dict() for item in listings]
            )
            if response.status_code == 201:
                self.logger.info(f"Sent {len(listings)} new items")
            else:
                self.logger.error(f"API Error: {response.status_code} - {response.text}")
        except Exception as e:
            self.logger.error(f"API send failed: {str(e)}")

    def run(self):
        """Start the WebSocket client"""
        self.logger.info("Starting Skinport WebSocket scraper")
        self.client.run()
