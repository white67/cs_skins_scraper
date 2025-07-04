import datetime
import logging
from typing import Optional
from .base_model import Listing
from config import SKINPORT_LISTING_URL, SKINPORT_MARKETPLACE
from config import STEAM_ICON_URL
from utils import convert_currency_str_to_symbol

class SkinportParser:
    """Parser implementation for Skinport marketplace listings"""
    
    @classmethod
    def parse(cls, raw: dict) -> Listing:
        """Main entry point for parsing Skinport listings"""
        return Listing(
            # Core item metadata
            item_name=cls._get_item_name(raw.get("title"), raw.get("name")),
            market_hash_name=raw.get("marketHashName"),
            item_type=raw.get("category"),
            item_type_category=raw.get("subCategory"),
            
            # Item specifics
            def_index=raw.get("itemId"),
            paint_index=raw.get("finish"),
            paint_seed=raw.get("pattern"),
            float_value=raw.get("wear"),
            icon_url=cls._build_icon_url(raw.get("image")),
            
            # Item traits
            is_stattrak=raw.get("stattrak", False),
            is_souvenir=raw.get("souvenir", False),
            rarity=raw.get("rarity"),
            wear=raw.get("exterior"),
            
            # Trade and lock info
            tradable=cls._is_tradable(raw.get("lock")),
            lock_timestamp=cls._parse_lock_timestamp(raw.get("lock")),
            
            # Listing details
            inspect_link=raw.get("link"),
            item_collection=raw.get("collection"),
            price=cls._parse_price(raw.get("salePrice")),
            price_currency=raw.get("currency"),
            price_currency_symbol=convert_currency_str_to_symbol(raw.get("currency")),
            listing_id=str(raw.get("saleId")),
            listing_url=cls._build_listing_url(raw.get("url"), raw.get("saleId")),
            listing_timestamp=cls._parse_timestamp(raw.get("created_at")),
            
            # Marketplace info
            marketplace=SKINPORT_MARKETPLACE,
            status=raw.get("saleStatus"),
        )
    
    # Helper methods
    
    @staticmethod
    def _get_item_name(title: Optional[str], name: Optional[str]) -> str:
        """Construct full item name from title and name components"""
        if not title or not name:
            return ""
        return f"{title.replace('StatTrak™', '').strip()} | {name}"
    
    @classmethod
    def _build_listing_url(cls, base_url: Optional[str], sale_id: Optional[str]) -> Optional[str]:
        """Construct full listing URL"""
        if not sale_id or not base_url:
            return None
        return f"{SKINPORT_LISTING_URL}{base_url}/{sale_id}"
    
    @staticmethod
    def _build_icon_url(icon_path: Optional[str]) -> Optional[str]:
        """Generate full Steam CDN URL from icon path"""
        return f"{STEAM_ICON_URL}{icon_path}" if icon_path else None
    
    @staticmethod
    def _is_tradable(lock_status: Optional[str]) -> bool:
        """Determine if item is currently tradable"""
        return lock_status not in [None, "None", ""]
    
    @staticmethod
    def _parse_lock_timestamp(lock_data: Optional[dict]) -> Optional[int]:
        """Extract lock expiration timestamp from raw data"""
        if not isinstance(lock_data, dict) or "seconds" not in lock_data:
            #logging.error(f"Unexpected lock_data format: {lock_data}")
            return None

        try:
            lock_dt = datetime.datetime.fromtimestamp(lock_data["seconds"])
            now = datetime.datetime.now()
            delta = lock_dt - now
            return delta.days
        except Exception as e:
            #logging.error(f"Error parsing lock timestamp: {e}")
            return None
    
    @staticmethod
    def _parse_price(raw_price: Optional[int]) -> float:
        """Convert raw price to decimal value"""
        return round(float(raw_price) / 100, 2) if raw_price else 0.0
    
    @staticmethod
    def _parse_timestamp(created_at: Optional[str]) -> int:
        """Convert Skinport timestamp to UNIX timestamp"""
        if not created_at:
            return int(datetime.datetime.now().timestamp())
            
        try:
            # Example format: "2024-05-01T12:34:56Z"
            dt = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            return int(dt.timestamp())
        except ValueError:
            return int(datetime.datetime.now().timestamp())