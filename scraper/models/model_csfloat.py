import datetime
from typing import Optional
from .base_model import Listing
from scraper.config import CSFLOAT_LISTING_URL, CSFLOAT_MARKETPLACE

class ListingCSFLOAT(Listing):
    """
    Extended version of base model - supporting CSFloat.
    """
    market_hash_name: str
    item_name: str
    created_at: str
    price: int
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
    item_type: str
    item_description: Optional[str] = None
    item_collection: Optional[str] = None
    listing_id: int
    marketplace: str
    
    def __init__(self, listing: dict) -> None:
        item = listing["item"]
        
        # Prepare data for the parent class
        data = {
            "market_hash_name": item.get("market_hash_name", None),
            "item_name": item.get("item_name", None),
            "created_at": listing.get("created_at", None),
            "price": listing.get("price", None),
            "asset_id": item.get("asset_id", None),
            "def_index": item.get("def_index", None),
            "paint_index": item.get("paint_index", None),
            "paint_seed": item.get("paint_seed", None),
            "float_value": item.get("float_value", None),
            "icon_url": item.get("icon_url", None),
            "is_stattrak": item.get("is_stattrak", False),
            "is_souvenir": item.get("is_souvenir", False),
            "rarity": item.get("rarity_name", None),
            "wear": item.get("wear_name", None),
            "inspect_link": item.get("inspect_link", None),
            "item_type": item.get("type_name", None),
            "item_description": item.get("description", None),
            "item_collection": item.get("collection", None),
            "item_type_category": None,
            "tradable": True,  # Assuming all items are tradable on CSFLOAT
            "trade_ban_days": 0,  # Assuming no trade ban days for CSFLOAT
            "price_currency": "USD",  # Assuming USD for CSFLOAT
            "listing_id": listing.get("id", None),
            "listing_url": self.get_listing_url(listing.get("id", None)),  # Construct URL if needed
            "listing_timestamp": self.get_listing_timestamp(listing["created_at"]),
            "marketplace": CSFLOAT_MARKETPLACE
        }
        
        super().__init__(**data)
    
    def get_listing_url(self, listing_id) -> str:
        return f"{CSFLOAT_LISTING_URL}{listing_id}"
    
    def get_listing_timestamp(self, created_at) -> int:
        return int(datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp())
        
    def map_to_base(self) -> Listing:
        return Listing(
            item_name=self.item_name,
            market_hash_name=self.market_hash_name,
            item_type=self.item_type,
            item_type_category=None,  # Assuming no category for CSFLOAT
            def_index=self.def_index,
            paint_index=self.paint_index,
            paint_seed=self.paint_seed,
            float_value=self.float_value,
            icon_url=self.icon_url,
            is_stattrak=self.is_stattrak,
            is_souvenir=self.is_souvenir,
            rarity=self.rarity,
            wear=self.wear,
            tradable=True,  # Assuming all items are tradable on CSFLOAT
            trade_ban_days=0,  # Assuming no trade ban days for CSFLOAT
            inspect_link=self.inspect_link,
            item_description=self.item_description,
            item_collection=self.item_collection,
            price=float(self.price) / 100,  # Convert price to float, XYZ ~ X.YZ USD
            price_currency="USD",  # Assuming USD for CSFLOAT
            listing_id=self.listing_id,
            listing_url=self.listing_url,
            listing_timestamp=self.listing_timestamp,
            marketplace=self.marketplace
        )