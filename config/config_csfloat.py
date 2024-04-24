CSFLOAT_API_ITEMS_LIMIT = 50
CSFLOAT_PRICE_MIN = 650 # usd XYZ = X.YZ
MARKETPLACE_CSFLOAT = "csfloat"

URL_CSFLOAT_NEWEST = f"https://csfloat.com/api/v1/listings?limit={CSFLOAT_API_ITEMS_LIMIT}&sort_by=most_recent&min_price={CSFLOAT_PRICE_MIN}"

def csfloat_sale_link(item_id):
    return f"https://csfloat.com/item/{item_id}"
