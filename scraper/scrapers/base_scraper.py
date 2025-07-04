# base_scraper.py
import os
import json
import logging
import random
import time
from pathlib import Path
from typing import Type, List
from abc import ABC, abstractmethod
import requests
from models.base_model import BaseParser, Listing
from config import CACHE_FILE, LOGS_FILE, BACKEND_API_URL

class LimitedSizeDict:
    """In-memory cache with LRU eviction policy"""
    def __init__(self, max_size=1000):
        self.max_size = max_size
        self._cache = {}

    def __contains__(self, key):
        return key in self._cache

    def __setitem__(self, key, value):
        if len(self._cache) >= self.max_size:
            self._cache.pop(next(iter(self._cache)))
        self._cache[key] = value

    def update_from_json(self, data: list):
        """Load initial state from JSON"""
        for item in data:
            if "listing_id" in item:
                self._cache[item["listing_id"]] = item

class BaseScraper(ABC):
    def __init__(self, 
                 parser: Type[BaseParser],
                 marketplace_name: str,
                 cache_size: int = 1000,
                 request_timeout: int = 15):
        self.parser = parser
        self.marketplace_name = marketplace_name
        self.cache = LimitedSizeDict(max_size=cache_size)
        self.session = requests.Session()
        self.session.timeout = request_timeout
        self.consecutive_errors = 0
        self.logger = self._setup_logger()
        self._load_persistent_cache()

    @abstractmethod
    def fetch_raw_data(self) -> list[dict]:
        """Marketplace-specific data fetching implementation"""
        pass

    def process(self) -> List[Listing]:
        """Transform raw data to Listing objects"""
        try:
            raw_data = self.fetch_raw_data()
            # with open("xd.json", 'w') as log_file:
            #     json.dump(raw_data, log_file, indent=4)
            # self.logger.info(f"{raw_data}")
            return [self.parser.parse(item) for item in raw_data]
        except Exception as e:
            self.logger.error(f"Processing failed: {str(e)}")
            return []

    def run(self):
        """Main scraping loop"""
        while True:
            try:
                listings = self.process()
                new_items = self._filter_new(listings)
                
                if new_items:
                    self._send_to_api(new_items)
                    self._update_cache(new_items)
                    self._save_persistent_cache()

                sleep_time = self._get_interval()
                self.logger.info(f"Cycle complete. Sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)
                self.consecutive_errors = 0

            except Exception as e:
                self.consecutive_errors += 1
                sleep_time = self._get_error_interval()
                self.logger.error(f"Critical error: {str(e)}. Retrying in {sleep_time:.1f}s")
                time.sleep(sleep_time)

    # Helpers
    
    def _setup_logger(self):
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

    def _filter_new(self, listings: List[Listing]) -> List[Listing]:
        """Filter out already seen listings"""
        return [l for l in listings if l.listing_id not in self.cache]

    def _update_cache(self, new_items: List[Listing]):
        """Update in-memory cache"""
        for item in new_items:
            self.cache[item.listing_id] = item.dict()

    def _get_interval(self, base_interval: float = 25) -> float:
        """Get randomized interval with jitter"""
        jitter = random.uniform(0.8, 1.2)
        return base_interval * jitter

    def _get_error_interval(self) -> float:
        """Exponential backoff with jitter"""
        base = 2 ** self.consecutive_errors
        return random.uniform(1, min(base, 300))  # Max 5 minutes

    def _send_to_api(self, listings: List[Listing]):
        """Send new listings to backend"""
        try:
            response = requests.post(
                BACKEND_API_URL,
                json=[item.dict() for item in listings]
            )
            response.raise_for_status()
            self.logger.info(f"Sent {len(listings)} items to API")
        except Exception as e:
            self.logger.error(f"API send failed: {str(e)}")

    # Persistent cache management
    
    def _load_persistent_cache(self):
        """Load cache from JSON file"""
        cache_path = Path(CACHE_FILE) / f"{self.marketplace_name}_cache.json"
        
        try:
            if cache_path.exists():
                with open(cache_path) as f:
                    data = json.load(f)
                    self.cache.update_from_json(data)
        except Exception as e:
            self.logger.error(f"Cache load failed: {str(e)}")

    def _save_persistent_cache(self):
        """Save cache to JSON file"""
        cache_path = Path(CACHE_FILE) / f"{self.marketplace_name}_cache.json"
        
        try:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_path, 'w') as f:
                json.dump(list(self.cache._cache.values()), f)
        except Exception as e:
            self.logger.error(f"Cache save failed: {str(e)}")