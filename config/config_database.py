import mysql.connector
from mysql.connector import Error
from datetime import datetime

# credentials to database connection
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWD = "mansionmusik1400"
DB_DATABASE = "skins_valued"

MARKETPLACE_SKINPORT = "skinport"

BUFFIDS = "buffids"
BUFFIDS_ITEM_NAME = "item_name"
BUFFIDS_BUFF_ID = "buff_id"

BUFF_PRICES = "buff_prices"
BP_GOODS_ID = "goods_id"
BP_ITEM_FULL_NAME = "item_full_name"
BP_LOWEST_OFFER_CNY = "lowest_offer_cny"
BP_LOWEST_OFFER_PLN = "lowest_offer_pln"
BP_OFFERS_COUNT = "offers_count"
BP_HIGHEST_ORDER_CNY = "highest_order_cny"
BP_HIGHEST_ORDER_PLN = "highest_order_pln"
BP_ORDERS_COUNT = "orders_count"
BP_IMG = "img"
BP_LAST_UPDATE = "last_update"

SKIN_OFFERS = "skin_offers"
SO_OFFER_ID = 'offer_id'
SO_SALE_ID = 'sale_id'
SO_ITEM_FULL_NAME = 'item_full_name'
SO_ITEM_NAME = 'item_name'
SO_STATTRAK = 'stattrak'
SO_SALE_PRICE = 'sale_price'
SO_SALE_CUR = 'sale_cur'
SO_SALE_PRICE_PLN = 'sale_price_pln'
SO_STATUS = 'sale_status'
SO_WEAR = 'wear'
SO_EXTERIOR = 'exterior'
SO_RARITY = 'rarity'
SO_ITEM_COLLECTION = 'item_collection'
SO_ITEM_CATEGORY = 'item_category'
SO_SOUVENIR = 'souvenir'
SO_STICKERS = 'stickers'
SO_PATTERN = 'pattern'
SO_FINISH = 'finish'
SO_INSPECT_LINK = 'inspect_link'
SO_CUSTOM_NAME = 'custom_name'
SO_WEAPON_NAME = 'weapon_name'
SO_URL_SLUG = 'url_slug'
SO_TRADE_BANNED = 'trade_banned'
SO_TRADE_BAN_END = 'trade_ban_end'
SO_SCRAPE_TIME = 'scrape_time'
SO_MARKETPLACE = 'marketplace'
SO_LAST_UPDATE = "last_update"
SO_PRICE_RATIO = "price_ratio"
SO_SALE_LINK = "sale_link"
SO_GOODS_ID = "goods_id"
SO_AUCTION_HASH = "auction_hash"
SO_IMAGE_URL = "image_url"


# connect with database
def db_connect():
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWD,
        database=DB_DATABASE
    )
    # set buffer
    cursor = db.cursor(buffered=True)
    return db, cursor


# close connection
def db_close(db, cursor):
    cursor.close()
    db.close()


# add to database
def db_add(db, cursor, table_name, columns, data):
    try:
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))
        query = f"""INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});"""
        cursor.execute(query, data)
        db.commit() 
        print(f"[{table_name}] Insertion successful!")
    except mysql.connector.Error as err:
        print("Error:", err)
        db.rollback()  # Rollback the transaction if an error occurs


# function to check if entry in database (in single table) already exists
def check_if_exist(cursor, table_name, columns, data):
    # Construct the WHERE clause dynamically based on the columns provided
    where_clause = " AND ".join(f"{column} = %s" for column in columns)
    query = f"SELECT * FROM {table_name} WHERE {where_clause}"
    cursor.execute(query, data)
    result = cursor.fetchone()
    # Check if any row was fetched (meaning there's already a duplicate entry)
    return False if result == None else True


def db_update(db, cursor, table_name, columns, data, columns_to_check, data_to_check):
    try:
        if len(data_to_check) == 0:
            where_clause = ''
            existance = True
            updated_data = data
        else:
            where_clause = " AND ".join(f"{column} = %s" for column in columns_to_check)
            where_clause = f" WHERE {where_clause}"
            existance = check_if_exist(cursor, table_name, columns_to_check, data_to_check)
            updated_data = data + data_to_check
            
        if existance:
            updated_str = ', '.join(f"{column} = %s" for column in columns)
            update_query = (f"UPDATE {table_name} SET {updated_str}{where_clause};")
            cursor.execute(update_query, updated_data)
            db.commit()
            print(f"[{table_name}] Entry updated successfully.")
        else:
            print(f"[{table_name}] Entry does not exist: {data_to_check}")
    except mysql.connector.Error as err:
        print("Error:", err)
        db.rollback()  # Rollback the transaction if an error occurs


def get_record(cursor, column_to_get, table_name, columns, data):
    where_clause = " AND ".join(f"{column} = %s" for column in columns)
    
    # Construct the SELECT query
    query = f"SELECT {column_to_get} FROM {table_name} WHERE {where_clause}"
    
    cursor.execute(query, data)
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        return None


def get_records(cursor, columns_to_get, table_name, columns, data):
    where_clause = " AND ".join(f"{column} = %s" for column in columns)
    select_clause = ", ".join(columns_to_get)
    # Construct the SELECT query
    query = f"SELECT {select_clause} FROM {table_name} WHERE {where_clause}"
    
    cursor.execute(query, data)
    result = cursor.fetchone()
    
    if result:
        return result
    else:
        return None