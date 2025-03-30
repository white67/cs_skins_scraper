from pydantic import BaseModel
from typing import Optional

class Listing(BaseModel):
    """
    Base model for items to be scraped.
    """
    id: Optional[int] = None
    item_name: str
    market_hash_name: str
    item_type: str
    item_type_category: Optional[str] = None
    def_index: Optional[int] = None
    paint_index: Optional[int] = None
    paint_seed: Optional[int] = None
    float_value: Optional[float] = None
    icon_url: str
    is_stattrak: Optional[bool] = False
    is_souvenir: Optional[bool] = False
    rarity: Optional[str] = None
    wear: Optional[str] = None
    tradable: bool
    trade_ban_days: Optional[int] = None
    inspect_link: Optional[str] = None
    item_description: Optional[str] = None
    item_collection: Optional[str] = None
    price: float
    price_currency: str
    listing_url: str
    listing_timestamp: int
    
    # class Config:
    #     orm_mode = True  # Enable ORM mode for SQLAlchemy compatibility