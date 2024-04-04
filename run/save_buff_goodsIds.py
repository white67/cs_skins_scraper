import sys
sys.path.append('')
from config.config import *
from config.config_database import *
from config.config_buff import *


def save_buff_goods_ids():
    # make connection
    db, mycursor = db_connect()
    
    ids = read_json_file(FILE_BUDFFIDS)
    for el in ids:
        db_add(db, mycursor, BUFFIDS, [BUFFIDS_ITEM_NAME, BUFFIDS_BUFF_ID], [el, ids[el]])
    
    # close connection
    db_close(db, mycursor)


if __name__ == "__main__":
    save_buff_goods_ids()