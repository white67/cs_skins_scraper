import sys
sys.path.append('')
from config.config import *
from config.config_database import *
from config.config_buff import *
import time


def get_buff_price(db, mycursor, goods_id):
    
    # check if price has been updated lately for this item
    records = get_records(mycursor, [BP_LOWEST_OFFER_PLN, BP_LAST_UPDATE], BUFF_PRICES, [BP_GOODS_ID], [goods_id])
    
    if records:
        record_price_pln = records[0]
        last_update = records[1]
        
        result = check_time_difference(datetime.now(), last_update)
        
        if result:
            # print("Price within 5 days...")
            price_buff_pln = record_price_pln
        else:
            # print("Price is not up-to-date, scraping...")
            time.sleep(sleep_random(API_TIMEOUT))
            response = requests.get(buff_api_item(goods_id), headers=API_HEADERS_BUFF)

            if response.status_code == 200:
                response = response.json()
                db_update(db, mycursor, BUFF_PRICES, [
                        BP_LOWEST_OFFER_CNY, 
                        BP_LOWEST_OFFER_PLN, 
                        BP_OFFERS_COUNT, 
                        BP_HIGHEST_ORDER_CNY, 
                        BP_HIGHEST_ORDER_PLN, 
                        BP_ORDERS_COUNT, 
                        BP_LAST_UPDATE
                    ], 
                    [
                        float(response["data"]["sell_min_price"]),
                        float(response["data"]["sell_min_price"])*CNY_PLN,
                        response["data"]["sell_num"],
                        float(response["data"]["buy_max_price"]),
                        float(response["data"]["buy_max_price"])*CNY_PLN,
                        response["data"]["buy_num"],
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ],
                    [
                        BP_GOODS_ID
                    ],
                    [
                        goods_id
                ])
                
                price_buff_pln = float(response["data"]["sell_min_price"])*CNY_PLN
    else:
        # print("Price has not been scraped...")
        time.sleep(sleep_random(API_TIMEOUT))
        response = requests.get(buff_api_item(goods_id), headers=API_HEADERS_BUFF)

        if response.status_code == 200:
            response = response.json()
            price_buff_pln = float(response["data"]["sell_min_price"])*CNY_PLN
            
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
                ], 
                [
                    goods_id,
                    response["data"]["name"],
                    float(response["data"]["sell_min_price"]),
                    float(response["data"]["sell_min_price"])*CNY_PLN,
                    response["data"]["sell_num"],
                    float(response["data"]["buy_max_price"]),
                    float(response["data"]["buy_max_price"])*CNY_PLN,
                    response["data"]["buy_num"],
                    response["data"]["goods_info"]["icon_url"],
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])
    
    return float(price_buff_pln)


# Check if the difference is less than or equal to 5 days
def check_time_difference(current_date, date2):
    difference = current_date - date2
    
    if difference <= timedelta(days=5):
        return True
    else:
        return False


if __name__ == "__main__":
    db, mycursor = db_connect()
    price = get_buff_price(db, mycursor, 42399)
    print(price)
    print(type(price))