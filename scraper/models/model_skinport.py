import datetime
from typing import Optional
from .base_model import Listing
from scraper.config import SKINPORT_LISTING_URL, SKINPORT_MARKETPLACE

class ListingSKINPORT(Listing):
    """
    Extended version of base model - supporting SKINPORT.
    """
    market_hash_name: str
    item_name: str
    created_at: Optional[str] = None
    price: int
    price_currency: str
    asset_id: Optional[int] = None
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
    lock_timestamp: Optional[int] = None
    item_type: str
    tradable: bool
    item_description: Optional[str] = None
    item_collection: Optional[str] = None
    item_type_category: Optional[str] = None
    listing_id: int
    listing_url: str
    listing_timestamp: int
    marketplace: str
    
    def __init__(self, listing: dict) -> None:
        
        # Prepare data for the parent class
        data = {
            "market_hash_name": listing.get("marketHashName", None),
            "item_name": self.get_item_name(listing.get("title", None), listing.get("name", None)),
            "created_at": listing.get("created_at", None), # None
            "price": listing.get("salePrice", None), # random currency
            "asset_id": listing.get("assetid", None),
            "def_index": listing.get("itemId", None), # no idea
            "paint_index": listing.get("finish", None), # no idea
            "paint_seed": listing.get("pattern", None), # pattern
            "float_value": listing.get("wear", None),
            "icon_url": listing.get("image", None),
            "is_stattrak": listing.get("stattrak", False),
            "is_souvenir": listing.get("souvenir", False),
            "rarity": listing.get("rarity", None),
            "wear": listing.get("exterior", None),
            "inspect_link": listing.get("link", None),
            "item_type": listing.get("category", None),
            "item_description": None,
            "item_collection": listing.get("collection", None),
            "item_type_category": listing.get("subCategory", None),
            "tradable": self.get_tradable(listing.get("lock", None)),  # Assuming all items are tradable on CSFLOAT
            "lock_timestamp": self.get_lock_timestamp(listing.get("lock", None)),
            "price_currency": listing.get("currency", None),
            "listing_id": listing.get("saleId", None),
            "listing_url": self.get_listing_url(listing.get("url", None), listing.get("saleId", None)),  # Construct URL if needed
            "listing_timestamp": self.get_listing_timestamp(),
            "marketplace": SKINPORT_MARKETPLACE
        }
        
        super().__init__(**data)
    
    def get_item_name(self, title, name) -> str:
        return f"{title} | {name}"
    
    def get_listing_url(self, url, saleId) -> str:
        return f"{SKINPORT_LISTING_URL}{url}{saleId}"
    
    def get_tradable(self, lock) -> bool:
        if lock is None:
            return False
        else:
            return True
    
    def get_lock_timestamp(self, lock_timestamp) -> int:
        if lock_timestamp is None:
            return None
        else:
            return int(datetime.datetime.strptime(lock_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp())
    
    def get_listing_timestamp(self) -> int:
        return int(datetime.datetime.now().timestamp())
        
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
            listing_id=self.listing_id,
            listing_url=self.listing_url,
            listing_timestamp=self.listing_timestamp,
            marketplace=self.marketplace
        )