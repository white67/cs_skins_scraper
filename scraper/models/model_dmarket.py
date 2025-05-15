import datetime
from typing import Optional
from .base_model import Listing
from scraper.config import DMARKET_LISTING_URL, DMARKET_MARKETPLACE
from scraper.config import SKINS_RARITIES
from scraper.utils import convert_currency_str_to_symbol

class ListingDMARKET(Listing):
    """
    Extended version of base model - supporting DMARKET.
    """
    market_hash_name: str
    item_name: str
    price: float
    price_currency: str = "USD" # Assuming EUR for SKINBID
    asset_id: Optional[str] = None
    def_index: Optional[int] = None
    paint_index: Optional[int] = None
    paint_seed: Optional[int] = None
    float_value: Optional[float] = None
    icon_url: str
    is_stattrak: Optional[bool] = False
    is_souvenir: Optional[bool] = False
    rarity: Optional[str] = None
    wear: Optional[str] = None
    inspect_link: Optional[str] = None
    item_type: str
    item_description: Optional[str] = None
    item_collection: Optional[str] = None
    listing_id: str
    listing_url: str
    marketplace: str
    status: str = "listed"
    
    def __init__(self, listing: dict) -> None:
        
        # Prepare data for the parent class
        data = {
            "market_hash_name": listing.get("title", None),
            "item_name": listing["extra"].get("name", None),
            "price": int(listing["price"].get("USD", None))/100,
            "asset_id": listing["extra"].get("inGameAssetID", None),
            "def_index": None,
            "paint_index": listing["extra"].get("paintIndex", None),
            "paint_seed": listing["extra"].get("paintSeed", None),
            "float_value": listing["extra"].get("floatValue", None),
            "icon_url": listing.get("image", None),
            "is_stattrak": True if "stattrak" in listing["extra"].get("category", None) else False,
            "is_souvenir": True if "souvenir" in listing["extra"].get("category", None) else False,
            "rarity": listing["extra"].get("quality", None),
            "wear": listing["extra"].get("exterior", None),
            "inspect_link": listing["extra"].get("inspectInGame", None),
            "item_type": listing["extra"].get("itemType", None),
            "item_description": None,
            "item_collection": listing["extra"]["collection"][0],
            "item_type_category": listing["extra"].get("itemType", None),
            "tradable": listing["extra"].get("tradable", None),
            "lock_timestamp": listing["extra"].get("tradeLockDuration", None) + listing.get("createdAt", None),
            "price_currency": "USD",
            "price_currency_symbol": convert_currency_str_to_symbol("USD"),
            "listing_id": listing["extra"].get("linkId", None),
            "listing_url": self.get_dmarket_listing_url(listing["extra"].get("linkId", None)),
            "listing_timestamp": listing.get("createdAt", None),
            "marketplace": DMARKET_MARKETPLACE,
        }
        
        super().__init__(**data)
        
    def get_dmarket_listing_url(self, auction_hash) -> str:
        return f"{DMARKET_LISTING_URL}{auction_hash}" if auction_hash else None
        
    def map_to_base(self) -> Listing:
        return Listing(
            item_name=self.item_name,
            market_hash_name=self.market_hash_name,
            item_type=self.item_type,
            item_type_category=self.item_type_category,
            def_index=self.def_index,
            paint_index=self.paint_index,
            paint_seed=self.paint_seed,
            float_value=self.float_value,
            icon_url=self.icon_url,
            is_stattrak=self.is_stattrak,
            is_souvenir=self.is_souvenir,
            rarity=self.rarity,
            wear=self.wear,
            tradable=self.tradable,
            lock_timestamp=self.lock_timestamp, 
            inspect_link=self.inspect_link,
            item_description=self.item_description,
            item_collection=self.item_collection,
            price=self.price,
            price_currency=self.price_currency,
            price_currency_symbol=self.price_currency_symbol,
            listing_id=self.listing_id,
            listing_url=self.listing_url,
            listing_timestamp=self.listing_timestamp,
            marketplace=self.marketplace,
            status=self.status
        )