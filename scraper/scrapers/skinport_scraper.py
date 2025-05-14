import requests
import os
import logging

from skinport import Client

from scraper.models.model_skinport import ListingSKINPORT
from scraper.config import BACKEND_API_URL, SKINPORT_MARKETPLACE

class SKINPORTScraperWS:
    def __init__(self):
        self.client = Client()
        self.marketplace_name = SKINPORT_MARKETPLACE
        self.logger = self.setup_logger()

        self.register_handlers()  # Register event handlers

    def setup_logger(self):
        """
        Setup the logger for the scraper.
        """
        
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)

        logger = logging.getLogger(self.marketplace_name)
        logger.setLevel(logging.INFO)

        log_file = os.path.join(log_dir, f"{self.marketplace_name}.log")
        handler = logging.FileHandler(log_file, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        if not logger.handlers:
            logger.addHandler(handler)
        return logger

    def register_handlers(self):
        """
        Register event handlers for the WebSocket client.
        """
        
        @self.client.listen("saleFeed")
        async def on_sale_feed(data):
            await self.handle_sale_feed(data)

        @self.client.listen("maintenanceUpdated")
        async def on_maintenance_updated(data):
            self.logger.info(f"Maintenance updated: {data}")

        @self.client.listen("steamStatusUpdated")
        async def on_steam_status_updated(data):
            self.logger.info(f"Steam status updated: {data}")

    async def handle_sale_feed(self, data):
        """
        Handle the sale feed event.
        """

        try:
            # print(f"New sale feed item: {data}")
            
            new_listings = []
            
            for el in data["sales"]:
                el["lock"] = str(el["lock"])
                listing = ListingSKINPORT(el).map_to_base().to_dict()
                new_listings.append(listing)
            
            # self.logger.info(f"New_listings: {new_listings}")
            
            response = requests.post(BACKEND_API_URL, json=new_listings)
            if response.status_code == 201:
                self.logger.info(f"Sent new item to backend: new listing batch ({len(new_listings)} items).")
            else:
                self.logger.error(f"API Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            self.logger.error(f"Request error: {str(e)}")

    def start(self):
        """
        Start the WebSocket client.
        """
        
        self.client.run()