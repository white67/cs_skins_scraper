import sys
sys.path.append('')
from config.config import *
from config.config_database import *
from config.config_dmarket import *
from run.get_buff_price import *
from run.send_webhook import *


def get_newest_offers_dmarket(db, mycursor, api_url):
    
    seen_offers = 0
    
    # get request
    response = requests.get(api_url, headers=API_HEADERS_DMARKET)

    # check api status code
    if response.status_code == 200:
        print("Code: 200")
        
        response = response.json()
        
        for item in response["objects"]:

            item_properties_type = []
            item_properties = []
            
            item_full_name = item["title"]
            item_properties_type.append(SO_ITEM_FULL_NAME)
            item_properties.append(item_full_name)
            
            auction_link_id = item["extra"]["linkId"]
            item_properties_type.append(SO_AUCTION_HASH)
            item_properties.append(auction_link_id)
            
            sale_exist = check_if_exist(mycursor, SKIN_OFFERS, [SO_AUCTION_HASH, SO_ITEM_FULL_NAME], [auction_link_id, item_full_name])
             
            if sale_exist:
                seen_offers += 1 
                continue
            else:
                # sale link
                sale_link = dmarket_sale_link(auction_link_id)
                item_properties_type.append(SO_SALE_LINK)
                item_properties.append(sale_link)
            
                # goods id
                goods_id = get_record(mycursor, BUFFIDS_BUFF_ID, BUFFIDS, [BUFFIDS_ITEM_NAME], [item_full_name])
                item_properties_type.append(SO_GOODS_ID)
                item_properties.append(goods_id)
                
                # sale price
                real_price_usd = float(item["price"]["USD"])/100
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
                        auction_link_id,
                        item_full_name,
                        real_price,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        sale_link,
                        MARKETPLACE_DMARKET,
                        goods_id
                    ])
                    continue
                
                # price ratio
                price_ratio = buff_price/real_price
                item_properties_type.append(SO_PRICE_RATIO)
                item_properties.append(price_ratio)
                
                # trade banned
                trade_banned = item["extra"]["tradable"]
                item_properties_type.append(SO_TRADE_BANNED)
                item_properties.append(trade_banned)

                # trade lock
                if not trade_banned:
                    if "tradeLock" in item["extra"]:
                        lock_days = item["extra"]["tradeLock"]
                        item_properties_type.append(SO_LOCK_DAYS)
                        item_properties.append(lock_days)
                else:
                    lock_days = 0
                    
                # stattrak
                isStattrak = True if item["extra"]["category"] == "stattrak™" else False
                item_properties_type.append(SO_STATTRAK)
                item_properties.append(isStattrak)
                
                # item category
                itemType = item["extra"]["itemType"]
                item_properties_type.append(SO_ITEM_CATEGORY)
                item_properties.append(itemType)
                
                # souvenir
                isSouvenir = True if item["extra"]["category"] == "souvenir" else False
                item_properties_type.append(SO_SOUVENIR)
                item_properties.append(isSouvenir)
                
                # stickers
                if "stickers" in item["extra"]:
                    num_of_stickers = len(item["extra"]["stickers"])
                    item_properties_type.append(SO_STICKERS)
                    item_properties.append(num_of_stickers)
                    
                # exterior
                if "exterior" in item["extra"]:
                    exterior = item["extra"]["exterior"]
                    item_properties_type.append(SO_EXTERIOR)
                    item_properties.append(exterior)
                
                # float value
                if "floatValue" in item["extra"]:
                    floatValue = item["extra"]["floatValue"]
                    item_properties_type.append(SO_WEAR)
                    item_properties.append(floatValue)
                else:
                    floatValue = ""
                    
                # paint index / pattern
                if "paintIndex" in item["extra"]:
                    pattern = item["extra"]["paintIndex"]
                    item_properties_type.append(SO_PATTERN)
                    item_properties.append(pattern)
                
                # finish
                if "paintSeed" in item["extra"]:
                    finish = item["extra"]["paintSeed"]
                    item_properties_type.append(SO_FINISH)
                    item_properties.append(finish)
                    
                # inspect link
                if "inspectInGame" in item["extra"]:
                    inspectInGame = item["extra"]["inspectInGame"]
                    item_properties_type.append(SO_INSPECT_LINK)
                    item_properties.append(inspectInGame)
                
                # scape time
                datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item_properties_type.append(SO_SCRAPE_TIME)
                item_properties.append(datetime_now)
                
                # marketplace
                item_properties_type.append(SO_MARKETPLACE)
                item_properties.append(MARKETPLACE_DMARKET)
                
                # save_json_file("dmarket-test.json", response)
                
                # save to database
                db_add(db, mycursor, SKIN_OFFERS, item_properties_type, item_properties)
                
                if price_ratio >= RATIO_MIN and real_price > PRICE_MIN:
                    buff_img = get_record(mycursor, BP_IMG, BUFF_PRICES, [BP_GOODS_ID], [goods_id])
                    send_webhook(MARKETPLACE_DMARKET, item_full_name, round(real_price,2), round(buff_price,2), price_ratio, sale_link, buff_img, lock_days, floatValue, goods_id)
    
    # return offer_info
    return seen_offers


def keep_scraping_newest():
    
    
    # make connection
    db, mycursor = db_connect()
    
    counter = 0
    while True:
        counter += 1
        get_newest_offers_dmarket(db, mycursor, URL_DMARKET_NEWEST)
        print(f"{counter}. DMarket | Sleeping for {DMARKET_TIMEOUT} seconds...")
        time.sleep(sleep_random(DMARKET_TIMEOUT))
    
    # close connection
    db_close(db, mycursor)


if __name__ == "__main__":
    # make connection
    # db, mycursor = db_connect()
    # get_newest_offers_dmarket(db, mycursor, URL_DMARKET_NEWEST)
    
    
    keep_scraping_newest()