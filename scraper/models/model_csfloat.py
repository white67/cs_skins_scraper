import datetime
from typing import Optional
from .base_model import Listing
from config import CSFLOAT_LISTING_URL, CSFLOAT_MARKETPLACE
from config import STEAM_ICON_URL
from utils import convert_currency_str_to_symbol

class CSFloatParser:
    """Parser implementation for CSFloat marketplace listings"""
    
    @classmethod
    def parse(cls, raw: dict) -> Listing:
        """Main entry point for parsing CSFloat listings"""
        item = raw.get("item", {})
        
        return Listing(
            item_name=item.get("item_name"),
            market_hash_name=item.get("market_hash_name"),
            item_type=item.get("type_name"),
            item_type_category=None,
            
            def_index=item.get("def_index"),
            paint_index=item.get("paint_index"),
            paint_seed=item.get("paint_seed"),
            float_value=item.get("float_value"),
            icon_url=cls._build_icon_url(item.get("icon_url")),
            
            is_stattrak=item.get("is_stattrak", False),
            is_souvenir=item.get("is_souvenir", False),
            rarity=item.get("rarity_name"),
            wear=item.get("wear_name"),
            
            tradable=True,  # CSFloat items are always tradable
            lock_timestamp=None,
            
            inspect_link=item.get("inspect_link"),
            item_description=item.get("description"),
            item_collection=item.get("collection"),
            price=cls._parse_price(raw.get("price")),
            price_currency="USD",
            price_currency_symbol="$",
            listing_id=str(raw.get("id")),
            listing_url=cls._build_listing_url(raw.get("id")),
            listing_timestamp=cls._parse_timestamp(raw.get("created_at")),
            
            # Marketplace info
            marketplace=CSFLOAT_MARKETPLACE,
            status=raw.get("status", "listed")
        )

    # Helper methods ==========================================================
    
    @classmethod
    def _build_listing_url(cls, listing_id: Optional[str]) -> Optional[str]:
        """Construct full listing URL"""
        return f"{CSFLOAT_LISTING_URL}{listing_id}" if listing_id else None

    @staticmethod
    def _build_icon_url(icon_path: Optional[str]) -> Optional[str]:
        """Generate full Steam CDN URL from icon path"""
        return f"{STEAM_ICON_URL}{icon_path}" if icon_path else None

    @staticmethod
    def _parse_price(raw_price: Optional[int]) -> float:
        """Convert cents to dollars"""
        return round(float(raw_price) / 100, 2) if raw_price else 0.0

    @staticmethod
    def _parse_timestamp(created_at: Optional[str]) -> int:
        """Convert CSFloat timestamp to UNIX timestamp"""
        if not created_at:
            return int(datetime.datetime.now().timestamp())
            
        try:
            # Example format: "2024-05-01T12:34:56.789Z"
            dt = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            return int(dt.timestamp())
        except ValueError:
            return int(datetime.datetime.now().timestamp())
