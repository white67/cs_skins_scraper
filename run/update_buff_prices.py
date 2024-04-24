import sys
sys.path.append('')
from config.config import *
from config.config_database import *
from config.config_buff import *
import time

CAT = "category"
CATG = "category_group"
CATG_KNIFE = "knife"
CATG_GLOVES = "hands"
CATG_RIFLES = "rifle"
CATG_PISTOLS = "pistol"
CATG_SMGS = "smg"
CATG_SHOTGUNS = "shotgun"
CATG_MACHINEGUNS = "machinegun"
CATG_AGENTS = "type_customplayer"
CAT_CASES = "csgo_type_weaponcase"
CATG_ALL = [
    CATG_KNIFE,
    CATG_GLOVES,
    CATG_RIFLES,
    CATG_PISTOLS,
    CATG_SMGS,
    CATG_SHOTGUNS,
    CATG_MACHINEGUNS,
    CATG_AGENTS
]
CAT_ALL = [
    CAT_CASES
]

BUFF_CAT_ITEMS_LIMIT = 80
BUFF_TIMEOUT = 10


def buff_url_cat(cat_type, category, pagenum):
    return f"https://buff.163.com/api/market/goods?game=csgo&page_num={pagenum}&page_size={BUFF_CAT_ITEMS_LIMIT}&{cat_type}={category}&tab=selling&use_suggestion=0"


def update_prices_cat(db, mycursor):
    # for every category group
    for category in CAT_ALL:
        
        page_counter = 1
        total_pages = 10
        
        while page_counter <= total_pages:
            # get request
            url = buff_url_cat(CAT, category, page_counter)
            response = requests.get(url, headers=API_HEADERS_BUFF)
            
            # if good request
            if response.status_code == 200:
                response = response.json()
                print(response)
                
                # get total pages to scrape
                if page_counter == 1:
                    total_pages = response["data"]["total_page"]
                
                # for every item update price
                for item in response["data"]["items"]:
                    goods_id = int(item["id"])
                    entry_exist = check_if_exist(mycursor, BUFF_PRICES, [BP_GOODS_ID], [goods_id])
                    
                    print(f"{goods_id} | {item["name"]} | sell {float(item["sell_min_price"])*CNY_PLN} pln | buy {float(item["buy_max_price"])*CNY_PLN} pln")
                    
                    if entry_exist:
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
                                float(item["sell_min_price"]),
                                float(item["sell_min_price"])*CNY_PLN,
                                float(item["sell_num"]),
                                float(item["buy_max_price"]),
                                float(item["buy_max_price"])*CNY_PLN,
                                float(item["buy_num"]),
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            ],
                            [
                                BP_GOODS_ID
                            ],
                            [
                                goods_id
                            ]
                        )
                    else:
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
                                item["name"],
                                float(item["sell_min_price"]),
                                float(item["sell_min_price"])*CNY_PLN,
                                float(item["sell_num"]),
                                float(item["buy_max_price"]),
                                float(item["buy_max_price"])*CNY_PLN,
                                float(item["buy_num"]),
                                item["goods_info"]["icon_url"],
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            ]
                        )
            
            print(f"Sleeping {BUFF_TIMEOUT} seconds...")
            time.sleep(sleep_random(BUFF_TIMEOUT))
            page_counter += 1


def update_prices_catg(db, mycursor):
    # for every category group
    c = 1
    l = len(CATG_ALL)
    for category in CATG_ALL:
        print(f"#### {c}/{l}")
        
        page_counter = 1
        total_pages = 10
        
        while page_counter <= total_pages:
            # get request
            url = buff_url_cat(CATG, category, page_counter)
            response = requests.get(url, headers=API_HEADERS_BUFF)
            
            # if good request
            if response.status_code == 200:
                response = response.json()
                print(response)
                
                # get total pages to scrape
                if page_counter == 1:
                    total_pages = response["data"]["total_page"]
                
                # for every item update price
                for item in response["data"]["items"]:
                    goods_id = int(item["id"])
                    entry_exist = check_if_exist(mycursor, BUFF_PRICES, [BP_GOODS_ID], [goods_id])
                    
                    print(f"{goods_id} | {item["name"]} | sell {float(item["sell_min_price"])*CNY_PLN} pln | buy {float(item["buy_max_price"])*CNY_PLN} pln")
                    
                    if entry_exist:
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
                                float(item["sell_min_price"]),
                                float(item["sell_min_price"])*CNY_PLN,
                                float(item["sell_num"]),
                                float(item["buy_max_price"]),
                                float(item["buy_max_price"])*CNY_PLN,
                                float(item["buy_num"]),
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            ],
                            [
                                BP_GOODS_ID
                            ],
                            [
                                goods_id
                            ]
                        )
                    else:
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
                                item["name"],
                                float(item["sell_min_price"]),
                                float(item["sell_min_price"])*CNY_PLN,
                                float(item["sell_num"]),
                                float(item["buy_max_price"]),
                                float(item["buy_max_price"])*CNY_PLN,
                                float(item["buy_num"]),
                                item["goods_info"]["icon_url"],
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            ]
                        )
            
            print(f"Sleeping {BUFF_TIMEOUT} seconds...")
            print(f"#### {c}/{l}")
            time.sleep(sleep_random(BUFF_TIMEOUT))
            page_counter += 1
        c += 1


if __name__ == "__main__":
    db, mycursor = db_connect()
    
    # update_prices_cat(db, mycursor)
    update_prices_catg(db, mycursor)
    
    db_close(db, mycursor)