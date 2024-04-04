import sys
sys.path.append('')

# buff
FILE_BUDFFIDS = 'database/buffids.json'

API_HEADERS_BUFF = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Cookie': 'Device-Id=BGPsVUlaN0dcDxaXmrqn; Locale-Supported=en; game=csgo; session=1-w92KtZYfBULSJr-VKjMT2kwScEMbCrXLUAGqxES1VaeS2034437484; csrf_token=IjA2ZWMyYTQ1N2I3NjNmNzM5MjE3NjZlMWQ1NGYyYmRlMmU4NWJkODMi.GPB37w.XvLr1zPCo4cc4j1aBwHO-wkxmMs'
}

def buff_api_item(goods_id):
    return f"https://buff.163.com/api/market/goods/info?game=csgo&goods_id={goods_id}"

def buff_api_buy(goods_id): 
    return f"https://buff.163.com/api/market/goods/buy_order?game=csgo&goods_id={goods_id}&page_num=1"

def buff_api_sell(goods_id): 
    return f"https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={goods_id}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1"

def buff_api_history(goods_id): 
    return f"https://buff.163.com/api/market/goods/bill_order?game=csgo&goods_id={goods_id}"

class GoodsInfoItem:
    def __init__(
        self,
        goods_id: int,
        item_full_name: str,
        lowest_offer_cny: float,
        lowest_offer_pln: float,
        offers_count: int,
        highest_order_cny: float,
        highest_order_pln: float,
        orders_count: int,
        img: str,
        last_update: str
    ) -> None:
        self.goods_id: goods_id
        self.item_full_name: item_full_name
        self.lowest_offer_cny: lowest_offer_cny
        self.lowest_offer_pln: lowest_offer_pln
        self.offers_count: offers_count
        self.highest_order_cny: highest_order_cny
        self.highest_order_pln: highest_order_pln
        self.orders_count: orders_count
        self.img: img
        self.last_update: last_update