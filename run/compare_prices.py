import sys
sys.path.append('')
from config.config import *
from config.config_database import *
from config.config_buff import *
from run.get_buff_item_price import *


def compare_prices_to_buff(skin_full_name, price_pln):
    # make connection
    db, mycursor = db_connect()
    
    # find goods id
    goods_id = get_record(mycursor, BUFFIDS_BUFF_ID, BUFFIDS, [BUFFIDS_ITEM_NAME], [skin_full_name])
    
    price_buff_pln = get_buff_price(goods_id)
    
    return float(price_buff_pln)/float(price_pln)
    

if __name__ == "__main__":
    
    skin_full_name = "Tec-9 | Red Quartz (Factory New)"
    price_pln = 0.91
    
    compare_prices_to_buff(skin_full_name, price_pln)