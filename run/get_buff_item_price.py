import sys
sys.path.append('')
from config.config import *
from config.config_database import *
from config.config_buff import *
import time


def get_buff_price(goods_id):
    # make connection
    db, mycursor = db_connect()
    
    # check if price has been updated lately for this item
    update_history = check_if_exist(mycursor, BUFF_PRICES, [BP_GOODS_ID], [goods_id])
    
    if update_history:
        # check if price has been updated in last 5 days, if not, update
        last_update = get_record(mycursor, BP_LAST_UPDATE, BUFF_PRICES, [BP_GOODS_ID], [goods_id])
        # last_update = datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S")
        
        result = check_time_difference(datetime.now(), last_update)
        
        if result:
            print("Price within 5 days...")
            price_buff_pln = get_record(mycursor, BP_LOWEST_OFFER_PLN, BUFF_PRICES, [BP_GOODS_ID], [goods_id])
        else:
            print("Price is not up-to-date, scraping...")
            # scrape buff data but only update
            
            time.sleep(sleep_random(API_TIMEOUT))
            response = requests.get(buff_api_item(goods_id), headers=API_HEADERS_BUFF)

            # check api status code
            if response.status_code == 200:
                print("Code: 200")
                response = response.json()
                
                # update database
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
                
                print(response)
                price_buff_pln = float(response["data"]["sell_min_price"])*CNY_PLN
                
                # price_buff_pln = get_buff_price(goods_id)
    else:
        print("Price doesn't exist, scrape first...")
        # scrape buff data for the first time
        
        # get request
        time.sleep(sleep_random(API_TIMEOUT))
        response = requests.get(buff_api_item(goods_id), headers=API_HEADERS_BUFF)

        # check api status code
        if response.status_code == 200:
            print("Code: 200")
            
            response = response.json()
            
            # create object
            # item_info = GoodsInfoItem(
            #     goods_id,
            #     response["data"]["name"],
            #     response["data"]["sell_min_price"],
            #     response["data"]["sell_min_price"]*CNY_PLN,
            #     response["data"]["sell_num"],
            #     response["data"]["buy_max_price"],
            #     response["data"]["buy_max_price"]*CNY_PLN,
            #     response["data"]["buy_num"],
            #     response["data"]["buy_num"]["goods_info"]["icon_url"],
            #     datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # )
            
            # data = {
            #     BP_GOODS_ID: goods_id,
            #     BP_ITEM_FULL_NAME: response["data"]["name"],
            #     BP_LOWEST_OFFER_CNY: response["data"]["sell_min_price"],
            #     BP_LOWEST_OFFER_PLN: response["data"]["sell_min_price"]*CNY_PLN,
            #     BP_OFFERS_COUNT: response["data"]["sell_num"],
            #     BP_HIGHEST_ORDER_CNY: response["data"]["buy_max_price"],
            #     BP_HIGHEST_ORDER_PLN: response["data"]["buy_max_price"]*CNY_PLN,
            #     BP_ORDERS_COUNT: response["data"]["buy_num"],
            #     BP_IMG: response["data"]["buy_num"]["goods_info"]["icon_url"],
            #     BP_LAST_UPDATE: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # }
            
            # print(f"goods_id: {goods_id}")
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
    
    # close connection
    db_close(db, mycursor)
    
    return price_buff_pln


def check_time_difference(current_date, date2):
    difference = current_date - date2

    # Check if the difference is less than or equal to 5 days
    if difference <= timedelta(days=5):
        return True
    else:
        return False


if __name__ == "__main__":
    get_buff_price(34915)