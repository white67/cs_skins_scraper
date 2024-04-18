SKINBID_API_ITEMS_LIMIT = 50
SKINBID_PRICE_MIN = 28 # pln
MARKETPLACE_SKINBID = "skinbid"

URL_SKINBID_NEWEST = f"https://api.skinbid.com/api/search/auctions?take={SKINBID_API_ITEMS_LIMIT}&skip=0&sellType=fixed_price&sort=created%23desc&Pricegt={SKINBID_PRICE_MIN}&goodDeals=false&popular=false&currency=PLN"
URL_SKINBID_RABAT = f"https://api.skinbid.com/api/search/auctions?take={SKINBID_API_ITEMS_LIMIT}&skip=0&sellType=fixed_price&sort=discount%23desc&Pricegt={SKINBID_PRICE_MIN}&goodDeals=false&popular=false&currency=PLN"
URL_SKINBID_AUCTION_END_SOON = f"https://api.skinbid.com/api/search/auctions?take={SKINBID_API_ITEMS_LIMIT}&skip=0&sellType=auction&sort=time-left%23asc&Pricegt={SKINBID_PRICE_MIN}&goodDeals=false&popular=false&currency=PLN"


def skinbid_sale_link(auctionHash):
    return f"https://skinbid.com/market/{auctionHash}"


def url_skinbid_newest(i):
    return f"https://api.skinbid.com/api/search/auctions?take={SKINBID_API_ITEMS_LIMIT}&skip={SKINBID_API_ITEMS_LIMIT*i}&sellType=fixed_price&sort=created%23desc&Pricegt={SKINBID_PRICE_MIN}&goodDeals=false&popular=false&currency=PLN"
