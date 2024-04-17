import sys
sys.path.append('')
from config.config import *
from config.config_database import *
from config.config_skinport import *
from run.compare_prices import *
from run.send_webhook import *
from run.get_skinport_offers import *

def xxx():
    
    url22 = "https://skinport.com/api/browse/730?sort=date&order=desc&pricegt=700"
    
    # make connection
    db, mycursor = db_connect()
    
    # get request
    response = requests.get(url22, headers=API_HEADERS_SKINPORT)
    
    # check api status code
    if response.status_code == 200:
        print("Code: 200")
        
        response = response.json()
        
        save_json_file("testing_response.json", response)
    
    goods_id = get_record(mycursor, BUFFIDS_BUFF_ID, BUFFIDS, [BUFFIDS_ITEM_NAME], ["★ Sport Gloves | Pandora's Box (Battle-Scarred)"])
    
    response = requests.get(buff_api_item(goods_id), headers=API_HEADERS_BUFF)

    # check api status code
    if response.status_code == 200:
        print("Code: 200")
        response = response.json()
        
        save_json_file("testing_buff_response.json", response)


if __name__ == "__main__":
    xxx()