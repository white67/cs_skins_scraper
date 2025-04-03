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
    lock_timestamp: Optional[int] = None
    inspect_link: Optional[str] = None
    item_description: Optional[str] = None
    item_collection: Optional[str] = None
    price: float
    price_currency: str
    listing_id: int
    listing_url: str
    listing_timestamp: int
    marketplace: str
    
    # Convert the Listing object's attributes to a dictionary
    def to_dict(self):
        # without the first key
        return {
            key: value for key, value in self.__dict__.items() if key != 'id'
        }
        
    # Generate the INSERT query dynamically based on the attributes of the class
    def generate_insert_query(self):
        # Get the column names from the object's attributes
        dict_attributes = self.to_dict()
        columns = ', '.join(dict_attributes.keys())
        values = ', '.join(['%s'] * len(dict_attributes))

        # Create the INSERT query
        insert_query = f"INSERT INTO listings ({columns}) VALUES ({values})"
        return insert_query
    
    def to_db_tuple(self):
        """
        Convert the model instance to a tuple for database insertion.
        """
        return (
            self.item_name,
            self.market_hash_name,
            self.item_type,
            self.item_type_category,
            self.def_index,
            self.paint_index,
            self.paint_seed,
            self.float_value,
            self.icon_url,
            self.is_stattrak,
            self.is_souvenir,
            self.rarity,
            self.wear,
            self.tradable,
            self.lock_timestamp,
            self.inspect_link,
            self.item_description,
            self.item_collection,
            self.price,
            self.price_currency,
            self.listing_id,
            self.listing_url,
            self.listing_timestamp,
            self.marketplace
        )