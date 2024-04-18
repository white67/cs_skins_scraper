import sys
sys.path.append('')
from config.config import *
from config.config_database import *
from config.config_skinport import *
from run.get_buff_price import *
from run.send_webhook import *


def get_newest_offers_skinport(db, mycursor, api_url):
    
    seen_offers = 0
    
    # get request
    response = requests.get(api_url, headers=API_HEADERS_SKINPORT)

    # check api status code
    if response.status_code == 200:
        print("Code: 200")
        
        response = response.json()
        
        for item in response["items"]:
            
            sale_exist = check_if_exist(mycursor, SKIN_OFFERS, [SO_SALE_ID, SO_ITEM_FULL_NAME], [item["saleId"], item["marketHashName"]])
            
            sale_link = skinport_sale_link(item["saleId"], item["url"])
            goods_id = get_record(mycursor, BUFFIDS_BUFF_ID, BUFFIDS, [BUFFIDS_ITEM_NAME], [item["marketHashName"]])
            
            real_price = float(item["salePrice"]) / 100
            buff_price = get_buff_price(db, mycursor, goods_id)
            
            if buff_price == -1:
                print(f"error getting goods id: {item["marketHashName"]} | {goods_id}\nsleeping...")
                time.sleep(sleep_random(5))
                continue
            
            price_ratio = buff_price/real_price
            
            if item["lock"] == None:
                trade_ban_end = ""
                trade_banned = False 
            else: 
                trade_ban_end = datetime.strptime(item["lock"], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
                trade_banned = True
             
            if sale_exist:
                if item["lock"] == None:
                    db_update(db, mycursor, SKIN_OFFERS, [
                            SO_SALE_PRICE,
                            SO_SALE_CUR,
                            SO_SALE_PRICE_PLN,
                            SO_STATUS,
                            SO_TRADE_BANNED,
                            SO_LAST_UPDATE,
                            SO_PRICE_RATIO
                        ], 
                        [
                            real_price,
                            item["currency"],
                            real_price,
                            item["saleStatus"],
                            trade_banned,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            price_ratio
                        ], 
                        [
                            SO_SALE_ID, 
                            SO_ITEM_FULL_NAME
                        ], 
                        [
                            item["saleId"], 
                            item["marketHashName"]
                        ])
                else:
                    db_update(db, mycursor, SKIN_OFFERS, [
                            SO_SALE_PRICE,
                            SO_SALE_CUR,
                            SO_SALE_PRICE_PLN,
                            SO_STATUS,
                            SO_TRADE_BANNED,
                            SO_TRADE_BAN_END,
                            SO_LAST_UPDATE,
                            SO_PRICE_RATIO
                        ], 
                        [
                            real_price,
                            item["currency"],
                            real_price,
                            item["saleStatus"],
                            trade_banned,
                            trade_ban_end,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            price_ratio
                        ], 
                        [
                            SO_SALE_ID, 
                            SO_ITEM_FULL_NAME
                        ], 
                        [
                            item["saleId"], 
                            item["marketHashName"]
                        ])
                seen_offers += 1
                
                # if price_ratio >= RATIO_MIN and real_price > PRICE_MIN:
                #     buff_img = get_record(mycursor, BP_IMG, BUFF_PRICES, [BP_GOODS_ID], [goods_id])
                    
                #     if trade_ban_end != "":
                #         lock_days = trade_ban_days(trade_ban_end)
                #     else:
                #         lock_days = 0
                #     send_webhook("skinport", item["marketHashName"], round(real_price,2), round(buff_price,2), price_ratio, sale_link, buff_img, lock_days, item["wear"], goods_id)
                    
                continue
            
            if item["lock"] != None:
                # save to database
                db_add(db, mycursor, SKIN_OFFERS, [
                    SO_SALE_ID,
                    SO_ITEM_FULL_NAME,
                    SO_ITEM_NAME,
                    SO_STATTRAK,
                    SO_SALE_PRICE,
                    SO_SALE_CUR,
                    SO_SALE_PRICE_PLN,
                    SO_STATUS,
                    SO_WEAR,
                    SO_EXTERIOR,
                    SO_RARITY,
                    SO_ITEM_COLLECTION,
                    SO_ITEM_CATEGORY,
                    SO_SOUVENIR,
                    SO_STICKERS,
                    SO_PATTERN,
                    SO_FINISH,
                    SO_INSPECT_LINK,
                    SO_CUSTOM_NAME,
                    SO_WEAPON_NAME,
                    SO_URL_SLUG,
                    SO_TRADE_BANNED,
                    SO_TRADE_BAN_END,
                    SO_SCRAPE_TIME,
                    SO_MARKETPLACE,
                    SO_LAST_UPDATE,
                    SO_PRICE_RATIO,
                    SO_SALE_LINK,
                    SO_GOODS_ID
                ], 
                [
                    item["saleId"],
                    item["marketHashName"],
                    item["family"],
                    item["stattrak"],
                    real_price,
                    item["currency"],
                    real_price,
                    item["saleStatus"],
                    item["wear"],
                    item["exterior"],
                    item["rarity"],
                    item["collection"],
                    item["category"],
                    item["souvenir"],
                    len(item["stickers"]),
                    item["pattern"],
                    item["finish"],
                    item["link"],
                    f"{item["customName"]}",
                    item["subCategory"],
                    item["url"],
                    trade_banned,
                    trade_ban_end,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    MARKETPLACE_SKINPORT,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    price_ratio,
                    sale_link,
                    goods_id
                ])
            else:
                # save to database
                db_add(db, mycursor, SKIN_OFFERS, [
                SO_SALE_ID,
                SO_ITEM_FULL_NAME,
                SO_ITEM_NAME,
                SO_STATTRAK,
                SO_SALE_PRICE,
                SO_SALE_CUR,
                SO_SALE_PRICE_PLN,
                SO_STATUS,
                SO_WEAR,
                SO_EXTERIOR,
                SO_RARITY,
                SO_ITEM_COLLECTION,
                SO_ITEM_CATEGORY,
                SO_SOUVENIR,
                SO_STICKERS,
                SO_PATTERN,
                SO_FINISH,
                SO_INSPECT_LINK,
                SO_CUSTOM_NAME,
                SO_WEAPON_NAME,
                SO_URL_SLUG,
                SO_TRADE_BANNED,
                SO_SCRAPE_TIME,
                SO_MARKETPLACE,
                SO_LAST_UPDATE,
                SO_PRICE_RATIO,
                SO_SALE_LINK,
                SO_GOODS_ID
            ], 
            [
                item["saleId"],
                item["marketHashName"],
                item["family"],
                item["stattrak"],
                real_price,
                item["currency"],
                real_price,
                item["saleStatus"],
                item["wear"],
                item["exterior"],
                item["rarity"],
                item["collection"],
                item["category"],
                item["souvenir"],
                len(item["stickers"]),
                item["pattern"],
                item["finish"],
                item["link"],
                f"{item["customName"]}",
                item["subCategory"],
                item["url"],
                trade_banned,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                MARKETPLACE_SKINPORT,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                price_ratio,
                sale_link,
                goods_id
            ])
            
            if price_ratio >= RATIO_MIN and real_price > PRICE_MIN:
                buff_img = get_record(mycursor, BP_IMG, BUFF_PRICES, [BP_GOODS_ID], [goods_id])
                
                if trade_ban_end != "":
                    lock_days = trade_ban_days(trade_ban_end)
                else:
                    lock_days = 0
                send_webhook("skinport", item["marketHashName"], round(real_price,2), round(buff_price,2), price_ratio, sale_link, buff_img, lock_days, item["wear"], goods_id)
    
    
    # return offer_info
    return seen_offers


def keep_scraping_newest():
    
    db, mycursor = db_connect()
    
    while True:
        seen_offers = 0
        for i in range(0,10):
            if seen_offers > 5:
                break
            else:
                seen_offers += get_newest_offers_skinport(db, mycursor, url_skinport_newest(i))
        print(f"Sleeping for {SKINPORT_TIMEOUT} seconds...")
        time.sleep(sleep_random(SKINPORT_TIMEOUT))
    
    # close connection
    db_close(db, mycursor)


if __name__ == "__main__":
    keep_scraping_newest()
    
    # get_newest_offers_skinport(URL_SKINPORT_NEWEST)
    # get_newest_offers_skinport(URL_SKINPORT_RABAT)
    
    # for i in range(3):
    #     get_newest_offers_skinport(url_skinport_newest(i))
    
    # for i in range(6):
    #     get_newest_offers_skinport(url_skinport_rabat(i))