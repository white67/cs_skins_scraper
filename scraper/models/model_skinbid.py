import datetime
from typing import Optional
from .base_model import Listing
from config import SKINBID_LISTING_URL, SKINBID_MARKETPLACE, SKINS_RARITIES
from utils import convert_currency_str_to_symbol

class SkinBidParser:
    """Parser implementation for SkinBid marketplace listings"""
    
    @classmethod
    def parse(cls, raw: dict) -> Listing:
        """Main entry point for parsing SkinBid listings"""
        try:
            # Extract nested item and auction data from the response structure
            item_container = raw["items"][0]
            item_data = item_container["item"]
            auction_data = raw["auction"]
        except (KeyError, IndexError, TypeError) as e:
            raise ValueError(f"Invalid SkinBid data structure: {str(e)}")

        return Listing(
            # Core item metadata
            item_name=cls._get_base_name(item_data.get("subCategory"), item_data.get("name")),
            market_hash_name=item_data.get("fullName"),
            item_type=item_data.get("type"),
            item_type_category=item_data.get("category"),
            
            # Item specifics
            def_index=item_data.get("defIndex"),
            paint_index=item_data.get("paintIndex"),
            paint_seed=item_data.get("paintSeed"),
            float_value=item_data.get("float"),
            icon_url=item_data.get("imageUrl"),
            
            # Item traits
            is_stattrak=item_data.get("isStatTrak", False),
            is_souvenir=item_data.get("isSouvenir", False),
            rarity=cls._map_rarity(item_data.get("rarity")),
            wear=item_data.get("wearName"),
            
            # Trade and lock info
            tradable=not item_container.get("isTradeLocked", False),
            lock_timestamp=cls._parse_lock_timestamp(item_container.get("tradeLockExpireDate")),
            
            # Listing details
            inspect_link=item_data.get("inspectLink"),
            item_description=None,
            item_collection=item_data.get("collection"),
            price=raw.get("nextMinimumBid")
            price_currency="EUR",
            price_currency_symbol=convert_currency_str_to_symbol("EUR"),
            listing_id=auction_data.get("auctionHash"),
            listing_url=cls._build_listing_url(auction_data.get("auctionHash")),
            listing_timestamp=cls._parse_timestamp(auction_data.get("created")),
            
            # Marketplace info
            marketplace=SKINBID_MARKETPLACE,
            status="listed" if auction_data.get("isActive", False) else "ended"
        )

    # Helper methods ==========================================================
    
    @staticmethod
    def _get_base_name(sub_category: Optional[str], name: Optional[str]) -> str:
        """Construct base item name from components"""
        if not sub_category or not name:
            return ""
        return name if sub_category in name else f"{sub_category} | {name}"

    @staticmethod
    def _map_rarity(rarity_id: Optional[int]) -> Optional[str]:
        """Convert numeric rarity ID to text label"""
        return SKINS_RARITIES.get(rarity_id)

    @classmethod
    def _build_listing_url(cls, auction_hash: Optional[str]) -> Optional[str]:
        """Construct full marketplace listing URL"""
        return f"{SKINBID_LISTING_URL}{auction_hash}" if auction_hash else None

    @staticmethod
    def _parse_lock_timestamp(lock_date: Optional[str]) -> Optional[int]:
        """Convert trade lock date to UNIX timestamp"""
        if not lock_date:
            return None
        try:
            dt = datetime.datetime.strptime(lock_date, "%Y-%m-%dT%H:%M:%S")
            return int(dt.timestamp())
        except ValueError:
            return None

    @staticmethod
    def _parse_timestamp(created_at: Optional[str]) -> int:
        """Convert creation date to UNIX timestamp"""
        if not created_at:
            return int(datetime.datetime.now().timestamp())
        try:
            dt = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S")
            return int(dt.timestamp())
        except ValueError:
            return int(datetime.datetime.now().timestamp())

    @staticmethod
    def _parse_price(raw_price: Optional[float]) -> float:
        """Ensure price is valid floating point number"""
        try:
            return float(raw_price)
        except (TypeError, ValueError):
            return 0.0
