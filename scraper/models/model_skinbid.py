import datetime
from typing import Optional
from .base_model import Listing
from scraper.config import SKINBID_LISTING_URL, SKINBID_MARKETPLACE
from scraper.config import SKINS_RARITIES
from scraper.utils import convert_currency_str_to_symbol

class ListingSKINBID(Listing):
    """
    Extended version of base model - supporting SKINBID.
    """
    market_hash_name: str
    item_name: str
    price: float
    price_currency: str = "EUR" # Assuming EUR for SKINBID
    price_currency_symbol: Optional[str] = convert_currency_str_to_symbol("EUR")
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
    listing_id: str
    listing_url: str
    marketplace: str
    status: str = "listed"
    
    def __init__(self, listing: dict) -> None:
        item = listing["items"][0]
        auction = listing
        
        # Prepare data for the parent class
        data = {
            "market_hash_name": item["item"].get("fullName", None),
            "item_name": self.get_base_name(item["item"].get("subCategory", None), item["item"].get("name", None)),
            "price": auction.get("nextMinimumBid", None),
            "asset_id": item["item"].get("assetId", None),
            "def_index": item["item"].get("defIndex", None),
            "paint_index": item["item"].get("paintIndex", None),
            "paint_seed": item["item"].get("paintSeed", None),
            "float_value": item["item"].get("float", None),
            "icon_url": item["item"].get("imageUrl", None),
            "is_stattrak": item["item"].get("isStatTrak", False),
            "is_souvenir": item["item"].get("isSouvenir", False),
            "rarity": self.map_rarity(item["item"].get("rarity", None)),
            "wear": item["item"].get("wearName", None),
            "inspect_link": item["item"].get("inspectLink", None),
            "item_type": item["item"].get("type", None),
            "item_description": None,
            "item_collection": None,
            "item_type_category": item["item"].get("category", None),
            "tradable": item.get("tradeLockExpireDate", True) is None,
            "lock_timestamp": self.get_listing_timestamp(item.get("tradeLockExpireDate", None)),
            "price_currency": "EUR",
            "price_currency_symbol": convert_currency_str_to_symbol("EUR"),
            "listing_id": auction["auction"].get("auctionHash", None),
            "listing_url": self.get_skinbid_listing_url(auction["auction"].get("auctionHash", None)),
            "listing_timestamp": self.get_listing_timestamp(auction["auction"].get("created", None)),
            "marketplace": SKINBID_MARKETPLACE
        }
        
        super().__init__(**data)
        
    def get_base_name(self, subCategory, name) -> str:
        """
        Get the base name of the item.
        """
        if subCategory in name:
            return name
        else:
            return f"{subCategory} | {name}"
    
    def map_rarity(self, rarity) -> str:
        """
        Map numeric rarity to text.
        """
        return SKINS_RARITIES.get(rarity, None)
        
    def get_skinbid_listing_url(self, auction_hash) -> str:
        return f"{SKINBID_LISTING_URL}{auction_hash}" if auction_hash else None
    
    # 2025-05-14T19:04:29
    def get_listing_timestamp(self, created_at) -> int:
        return int(datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S").timestamp()) if created_at else None
        
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