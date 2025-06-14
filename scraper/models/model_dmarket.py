import datetime
from typing import Optional
from .base_model import Listing
from config import DMARKET_LISTING_URL, DMARKET_MARKETPLACE, SKINS_RARITIES
from utils import convert_currency_str_to_symbol

class DMarketParser:
    """Parser implementation for DMarket marketplace listings"""

    @classmethod
    def parse(cls, raw: dict) -> Listing:
        extra = raw.get("extra", {})
        price_info = raw.get("price", {})
        created_at = raw.get("createdAt")

        price = cls._parse_price(price_info.get("USD"))

        lock_timestamp = cls._parse_lock_timestamp(
            extra.get("tradeLockDuration"),
            created_at
        )

        # Parse listing timestamp
        listing_timestamp = cls._parse_timestamp(created_at)

        # Parse item collection (first element if it's a list)
        item_collection = None
        collection_val = extra.get("collection")
        if isinstance(collection_val, list) and collection_val:
            item_collection = collection_val[0]
        elif isinstance(collection_val, str):
            item_collection = collection_val

        # Parse tradable (bool)
        tradable = extra.get("tradable")
        if isinstance(tradable, str):
            tradable = tradable.lower() == "true"
        elif tradable is None:
            tradable = True  # default if not provided

        return Listing(
            market_hash_name=raw.get("title"),
            item_name=extra.get("name"),
            price=price,
            price_currency="USD",
            price_currency_symbol=convert_currency_str_to_symbol("USD"),
            asset_id=extra.get("inGameAssetID"),
            def_index=None,
            paint_index=extra.get("paintIndex"),
            paint_seed=extra.get("paintSeed"),
            float_value=extra.get("floatValue"),
            icon_url=raw.get("image"),
            is_stattrak=cls._parse_stattrak(extra.get("category")),
            is_souvenir=cls._parse_souvenir(extra.get("category")),
            rarity=cls._map_rarity(extra.get("quality")),
            wear=extra.get("exterior"),
            inspect_link=extra.get("inspectInGame"),
            item_type=extra.get("itemType"),
            item_description=None,
            item_collection=item_collection,
            item_type_category=extra.get("itemType"),
            tradable=tradable,
            lock_timestamp=lock_timestamp,
            listing_id=extra.get("linkId"),
            listing_url=cls._build_listing_url(extra.get("linkId")),
            listing_timestamp=listing_timestamp,
            marketplace=DMARKET_MARKETPLACE,
            status=raw.get("status", "listed")
        )

    # Helper methods ==========================================================

    @staticmethod
    def _parse_price(raw_price: Optional[int]) -> float:
        """Convert cents to dollars"""
        try:
            return round(float(raw_price) / 100, 2) if raw_price else 0.0
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _parse_stattrak(category: Optional[str]) -> bool:
        """Check if item is StatTrak"""
        return bool(category and "stattrak" in category.lower())

    @staticmethod
    def _parse_souvenir(category: Optional[str]) -> bool:
        """Check if item is Souvenir"""
        return bool(category and "souvenir" in category.lower())

    @staticmethod
    def _map_rarity(rarity: Optional[str]) -> Optional[str]:
        """Map DMarket rarity to your internal rarity, if needed"""
        if rarity is None:
            return None
        return SKINS_RARITIES.get(rarity, rarity)

    @classmethod
    def _build_listing_url(cls, link_id: Optional[str]) -> Optional[str]:
        """Build the listing URL"""
        return f"{DMARKET_LISTING_URL}{link_id}" if link_id else None

    @staticmethod
    def _parse_timestamp(created_at: Optional[str]) -> int:
        """Convert ISO timestamp to UNIX timestamp"""
        if not created_at:
            return int(datetime.datetime.now().timestamp())
        try:
            # Example: "2024-05-01T12:34:56Z" or "2024-05-01T12:34:56"
            fmt = "%Y-%m-%dT%H:%M:%SZ" if created_at.endswith("Z") else "%Y-%m-%dT%H:%M:%S"
            dt = datetime.datetime.strptime(created_at, fmt)
            return int(dt.timestamp())
        except Exception:
            return int(datetime.datetime.now().timestamp())

    @staticmethod
    def _parse_lock_timestamp(trade_lock_duration: Optional[int], created_at: Optional[str]) -> Optional[int]:
        """Calculate lock timestamp from duration and creation time"""
        if trade_lock_duration is None or created_at is None:
            return None
        try:
            # tradeLockDuration is in seconds, createdAt is ISO string
            fmt = "%Y-%m-%dT%H:%M:%SZ" if created_at.endswith("Z") else "%Y-%m-%dT%H:%M:%S"
            dt = datetime.datetime.strptime(created_at, fmt)
            return int(dt.timestamp()) + int(trade_lock_duration)
        except Exception:
            return None
