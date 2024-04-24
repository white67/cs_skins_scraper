SKINBID_API_ITEMS_LIMIT = 50
DMARKET_PRICE_MIN = 650 # usd XYZ = X.YZ
MARKETPLACE_DMARKET = "dmarket"

URL_DMARKET_NEWEST = f"https://api.dmarket.com/exchange/v1/market/items?side=market&orderBy=updated&orderDir=desc&title=&priceFrom={DMARKET_PRICE_MIN}&priceTo=0&treeFilters=&gameId=a8db&types=dmarket&cursor=&limit=100&currency=USD&platform=browser&isLoggedIn=true"


def dmarket_sale_link(offer_id):
    return f"https://dmarket.com/ingame-items/item-list/csgo-skins?userOfferId={offer_id}"