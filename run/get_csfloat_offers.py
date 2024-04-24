import sys
sys.path.append('')
from config.config import *
from config.config_database import *
from config.config_csfloat import *
from run.get_buff_price import *
from run.send_webhook import *


def get_newest_offers_csfloat(db, mycursor, api_url):
    
    seen_offers = 0
    
    # get request
    response = requests.get(api_url, headers=API_HEADERS_CSFLOAT)

    # check api status code
    if response.status_code == 200:
        print("Code: 200")
        
        response = response.json()
        
        for item in response:

            item_properties_type = []
            item_properties = []
            
            item_full_name = item["item"]["market_hash_name"]
            item_properties_type.append(SO_ITEM_FULL_NAME)
            item_properties.append(item_full_name)
            
            sale_id = item["id"]
            item_properties_type.append(SO_AUCTION_HASH)
            item_properties.append(sale_id)
            
            sale_exist = check_if_exist(mycursor, SKIN_OFFERS, [SO_AUCTION_HASH, SO_ITEM_FULL_NAME], [sale_id, item_full_name])
             
            if sale_exist:
                seen_offers += 1 
                continue
            else:
                # sale link
                sale_link = csfloat_sale_link(sale_id)
                item_properties_type.append(SO_SALE_LINK)
                item_properties.append(sale_link)
            
                # goods id
                goods_id = get_record(mycursor, BUFFIDS_BUFF_ID, BUFFIDS, [BUFFIDS_ITEM_NAME], [item_full_name])
                item_properties_type.append(SO_GOODS_ID)
                item_properties.append(goods_id)
                
                # sale price
                real_price_usd = float(item["price"])/100
                item_properties_type.append(SO_SALE_PRICE)
                item_properties.append(real_price_usd)
                
                # sale price pln
                real_price = real_price_usd * USD_PLN
                item_properties_type.append(SO_SALE_PRICE_PLN)
                item_properties.append(real_price)
                
                # price currency
                item_properties_type.append(SO_SALE_CUR)
                item_properties.append("USD")
                
                # get buff price from database
                item_price_from_db = get_record(mycursor, BP_LOWEST_OFFER_PLN, BUFF_PRICES, [BP_GOODS_ID], [goods_id])
                
                # if item's buff price has not been scraped, that means item is not worth trying, skip :)
                if item_price_from_db:
                    buff_price = float(item_price_from_db)
                else:
                    print("No buff price for this item, skip")
                    # save to database only to skip this offer next time
                    db_add(db, mycursor, SKIN_OFFERS, [
                        SO_AUCTION_HASH,
                        SO_ITEM_FULL_NAME,
                        SO_SALE_PRICE_PLN,
                        SO_LAST_UPDATE,
                        SO_SALE_LINK,
                        SO_MARKETPLACE,
                        SO_GOODS_ID
                    ], 
                    [
                        sale_id,
                        item_full_name,
                        real_price,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        sale_link,
                        MARKETPLACE_CSFLOAT,
                        goods_id
                    ])
                    continue
                
                # price ratio
                price_ratio = buff_price/real_price
                item_properties_type.append(SO_PRICE_RATIO)
                item_properties.append(price_ratio)
                
                # trade banned
                # trade_banned = item["extra"]["tradable"]
                # item_properties_type.append(SO_TRADE_BANNED)
                # item_properties.append(trade_banned)

                # trade lock
                lock_days = 0
                item_properties_type.append(SO_LOCK_DAYS)
                item_properties.append(lock_days)
                    
                # stattrak
                if "is_stattrak" in item["item"]:
                    isStattrak = item["item"]["is_stattrak"]
                    item_properties_type.append(SO_STATTRAK)
                    item_properties.append(isStattrak)
                
                # item category
                # itemType = item["extra"]["itemType"]
                # item_properties_type.append(SO_ITEM_CATEGORY)
                # item_properties.append(itemType)
                
                # souvenir
                if "is_souvenir" in item["item"]:
                    isSouvenir = item["item"]["is_souvenir"]
                    item_properties_type.append(SO_SOUVENIR)
                    item_properties.append(isSouvenir)
                
                # stickers
                if "stickers" in item["item"]:
                    num_of_stickers = len(item["item"]["stickers"])
                    item_properties_type.append(SO_STICKERS)
                    item_properties.append(num_of_stickers)
                    
                # exterior
                if "wear_name" in item["item"]:
                    exterior = item["item"]["wear_name"]
                    item_properties_type.append(SO_EXTERIOR)
                    item_properties.append(exterior)
                
                # float value
                if "float_value" in item["item"]:
                    floatValue = item["item"]["float_value"]
                    item_properties_type.append(SO_WEAR)
                    item_properties.append(floatValue)
                else:
                    floatValue = ""
                    
                # paint index / pattern
                if "paint_index" in item["item"]:
                    pattern = item["item"]["paint_index"]
                    item_properties_type.append(SO_PATTERN)
                    item_properties.append(pattern)
                
                # finish
                if "paint_seed" in item["item"]:
                    finish = item["item"]["paint_seed"]
                    item_properties_type.append(SO_FINISH)
                    item_properties.append(finish)
                    
                # inspect link
                # if "inspect_link" in item["item"]:
                #     inspectInGame = item["item"]["inspect_link"]
                #     item_properties_type.append(SO_INSPECT_LINK)
                #     item_properties.append(inspectInGame)
                
                # scape time
                datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item_properties_type.append(SO_SCRAPE_TIME)
                item_properties.append(datetime_now)
                
                # marketplace
                item_properties_type.append(SO_MARKETPLACE)
                item_properties.append(MARKETPLACE_CSFLOAT)
                
                # save_json_file("dmarket-test.json", response)
                
                # save to database
                db_add(db, mycursor, SKIN_OFFERS, item_properties_type, item_properties)
                
                if price_ratio >= RATIO_MIN and real_price > PRICE_MIN:
                    buff_img = get_record(mycursor, BP_IMG, BUFF_PRICES, [BP_GOODS_ID], [goods_id])
                    send_webhook(MARKETPLACE_CSFLOAT, item_full_name, round(real_price,2), round(buff_price,2), price_ratio, sale_link, buff_img, lock_days, floatValue, goods_id)
    
    # return offer_info
    return seen_offers


def keep_scraping_newest():
    
    
    # make connection
    db, mycursor = db_connect()
    
    counter = 0
    while True:
        counter += 1
        get_newest_offers_csfloat(db, mycursor, URL_CSFLOAT_NEWEST)
        print(f"{counter}. CSFloat | Sleeping for {CSFLOAT_TIMEOUT} seconds...")
        time.sleep(sleep_random(CSFLOAT_TIMEOUT))
    
    # close connection
    db_close(db, mycursor)


if __name__ == "__main__":
    # make connection
    # db, mycursor = db_connect()
    # get_newest_offers_dmarket(db, mycursor, URL_DMARKET_NEWEST)
    
    
    keep_scraping_newest()