import sys
sys.path.append('')
from config.config import *
from config.config_database import *
from config.config_buff import *


def get_price(goods_id):
    # make connection
    db, mycursor = db_connect()
    
    # get request
    response = requests.get(buff_api_item(goods_id), headers=API_HEADERS_BUFF)

    # check api status code
    if response.status_code == 200:
        print("Code: 200")
        
        response = response.json()
        
        # create object
        item_info = GoodsInfoItem(
            goods_id,
            response["data"]["name"],
            response["data"]["sell_min_price"],
            response["data"]["sell_min_price"]*CNY_PLN,
            response["data"]["sell_num"],
            response["data"]["buy_max_price"],
            response["data"]["buy_max_price"]*CNY_PLN,
            response["data"]["buy_num"],
            response["data"]["buy_num"]["goods_info"]["icon_url"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # save to database
        db_add(db, mycursor, BUFF_PRICES, [
            BP_GOODS_ID, 
            BP_ITEM_FULL_NAME, 
            BP_LOWEST_OFFER_CNY, 
            BP_LOWEST_OFFER_PLN, 
            BP_OFFERS_COUNT, 
            BP_HIGHEST_ORDER_CNY, 
            BP_HIGHEST_ORDER_PLN, 
            BP_ORDERS_COUNT, 
            BP_IMG, 
            BP_LAST_UPDATE
            ], [
            item_info.goods_id,
            item_info.item_full_name,
            item_info.lowest_offer_cny,
            item_info.lowest_offer_pln,
            item_info.offers_count,
            item_info.highest_order_cny,
            item_info.highest_order_pln,
            item_info.orders_count,
            item_info.img,
            item_info.last_update
        ])
    
    # close connection
    db_close(db, mycursor)
    
    return item_info


if __name__ == "__main__":
    get_price(34915)