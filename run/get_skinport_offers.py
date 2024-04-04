import sys
sys.path.append('')
from config.config import *
from config.config_database import *
from config.config_skinport import *
from run.compare_prices import *
from run.send_webhook import *


def get_newest_offers_skinport(api_url):
    # make connection
    db, mycursor = db_connect()
    
    # get request
    response = requests.get(api_url, headers=API_HEADERS_SKINPORT)

    # check api status code
    if response.status_code == 200:
        print("Code: 200")
        
        response = response.json()
        
        for item in response["items"]:
            
            sale_exist = check_if_exist(mycursor, SKIN_OFFERS, [SO_SALE_ID, SO_ITEM_FULL_NAME], [item["saleId"], item["marketHashName"]])
            
            sale_link = sale_link_url(item["saleId"], item["url"])
            goods_id = get_record(mycursor, BUFFIDS_BUFF_ID, BUFFIDS, [BUFFIDS_ITEM_NAME], [item["marketHashName"]])
            
            real_price = float(item["salePrice"]) / 100
            buff_price = compare_prices_to_buff(item["marketHashName"], real_price)
            
            if buff_price == -2:
                print(f"error getting goods id: {item["marketHashName"]}")
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
            
            buff_img = get_record(mycursor, BP_IMG, BUFF_PRICES, [BP_GOODS_ID], [goods_id])
            
            if price_ratio >= 0.94 and real_price > 0.5:
                send_webhook_skinport(item["marketHashName"], real_price, buff_price, price_ratio, sale_link, buff_img)
            
                # create object
                # offer_info = SkinportOfferInfo(
                #     item["saleId"],
                #     item["marketHashName"],
                #     item["family"],
                #     item["stattrak"],
                #     item["salePrice"],
                #     item["currency"],
                #     item["salePrice"],
                #     item["saleStatus"],
                #     item["wear"],
                #     item["exterior"],
                #     item["rarity"],
                #     item["collection"],
                #     item["category"],
                #     item["souvenir"],
                #     len(item["stickers"]),
                #     item["pattern"],
                #     item["finish"],
                #     item["link"],
                #     f"{item["customName"]}",
                #     item["subCategory"],
                #     item["url"],
                #     trade_banned,
                #     trade_ban_end,
                #     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                #     MARKETPLACE_SKINPORT,
                #     datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # )
    
    # close connection
    db_close(db, mycursor)
    
    # return offer_info


def keep_scraping_newest():
    while True:
        time.sleep(sleep_random(API_TIMEOUT)+3)
        for i in range(0,9):
            get_newest_offers_skinport(url_skinport_newest(i+1))


if __name__ == "__main__":
    # keep_scraping_newest()
    
    get_newest_offers_skinport(URL_SKINPORT_NEWEST)
    get_newest_offers_skinport(URL_SKINPORT_RABAT)
    
    for i in range(10):
        get_newest_offers_skinport(url_skinport_rabat(i+1))