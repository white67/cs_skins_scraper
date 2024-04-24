import sys
sys.path.append('')
from config.config import *
from config.config_database import *
from config.config_skinbid import *
from run.get_buff_price import *
from run.send_webhook import *


def get_newest_offers_skinbid(db, mycursor, api_url):
    
    seen_offers = 0
    
    # get request
    response = requests.get(api_url, headers=API_HEADERS_SKINBID)

    # check api status code
    if response.status_code == 200:
        print("Code: 200")
        
        response = response.json()
        
        for item in response["items"]:
            
            item_full_name = item["items"][0]["item"]["fullName"]
            auction_hash = item["auction"]["auctionHash"]
            
            sale_exist = check_if_exist(mycursor, SKIN_OFFERS, [SO_AUCTION_HASH, SO_ITEM_FULL_NAME], [auction_hash, item_full_name])
             
            if sale_exist:
                seen_offers += 1 
                continue
            else:
                sale_link = skinbid_sale_link(auction_hash)
                goods_id = get_record(mycursor, BUFFIDS_BUFF_ID, BUFFIDS, [BUFFIDS_ITEM_NAME], [item_full_name])
                
                real_price = float(item["nextMinimumBid"])
                
                # get buff price from database
                item_price_from_fb = get_record(mycursor, BP_LOWEST_OFFER_PLN, BUFF_PRICES, [BP_GOODS_ID], [goods_id])
                
                # if item's buff price has not been scraped, that means item is not worth trying, skip :)
                if item_price_from_fb:
                    buff_price = float(item_price_from_fb)
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
                        auction_hash,
                        item_full_name,
                        real_price,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        sale_link,
                        MARKETPLACE_SKINBID,
                        goods_id
                    ])
                    continue
                
                # if buff_price == -1:
                #     print(f"error getting buff price for: {item_full_name} | {goods_id}\nsleeping...")
                #     time.sleep(sleep_random(2))
                #     continue
                
                price_ratio = buff_price/real_price
                
                # SKINBID uses only P2P so no trade ban
                trade_ban_end = ""
                trade_banned = False
                lock_days = 0
                    
                # save to database
                db_add(db, mycursor, SKIN_OFFERS, [
                    SO_AUCTION_HASH,
                    SO_ITEM_FULL_NAME,
                    SO_ITEM_NAME,
                    SO_STATTRAK,
                    SO_SALE_PRICE,
                    SO_SALE_CUR,
                    SO_SALE_PRICE_PLN,
                    SO_WEAR,
                    SO_EXTERIOR,
                    SO_ITEM_CATEGORY,
                    SO_SOUVENIR,
                    SO_STICKERS,
                    SO_PATTERN,
                    SO_FINISH,
                    SO_INSPECT_LINK,
                    SO_WEAPON_NAME,
                    SO_SCRAPE_TIME,
                    SO_MARKETPLACE,
                    SO_LAST_UPDATE,
                    SO_PRICE_RATIO,
                    SO_SALE_LINK,
                    SO_GOODS_ID
                ], 
                [
                    auction_hash,
                    item_full_name,
                    item["items"][0]["item"]["name"],
                    item["items"][0]["item"]["isStatTrak"],
                    item["nextMinimumBidEur"],
                    "EUR",
                    real_price,
                    item["items"][0]["item"]["float"],
                    item["items"][0]["item"]["wearName"],
                    item["items"][0]["item"]["category"],
                    item["items"][0]["item"]["isSouvenir"],
                    len(item["items"][0]["item"]["stickers"]),
                    item["items"][0]["item"]["paintSeed"],
                    item["items"][0]["item"]["paintIndex"],
                    item["items"][0]["item"]["inspectLink"],
                    item["items"][0]["item"]["subCategory"],
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    MARKETPLACE_SKINBID,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    price_ratio,
                    sale_link,
                    goods_id
                ])
                
                if price_ratio >= RATIO_MIN and real_price > PRICE_MIN:
                    buff_img = get_record(mycursor, BP_IMG, BUFF_PRICES, [BP_GOODS_ID], [goods_id])
                    send_webhook(MARKETPLACE_SKINBID, item_full_name, round(real_price,2), round(buff_price,2), price_ratio, sale_link, buff_img, lock_days, item["items"][0]["item"]["float"], goods_id)
    
    # return offer_info
    return seen_offers


def keep_scraping_newest():
    
    # make connection
    db, mycursor = db_connect()
    
    counter = 0
    while True:
        counter += 1
        seen_offers = 0
        for i in range(0,5):
            if seen_offers > 5:
                break
            else:
                seen_offers += get_newest_offers_skinbid(db, mycursor, url_skinbid_newest(i))
        print(f"{counter}. Skinbid | Sleeping for {SKINBID_TIMEOUT} seconds...")
        time.sleep(sleep_random(SKINBID_TIMEOUT))
    
    # close connection
    db_close(db, mycursor)


if __name__ == "__main__":
    keep_scraping_newest()
        
    # get_newest_offers_skinbid(url_skinbid_newest(0))