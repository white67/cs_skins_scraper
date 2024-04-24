import sys
import random
sys.path.append('')
import requests
import json
from datetime import datetime, timedelta, timezone




CNY_PLN = 0.556
USD_PLN = 4.046
API_TIMEOUT = 2 # seconds
SKINPORT_TIMEOUT = 8 # seconds
SKINBID_TIMEOUT = 8 # seconds
DMARKET_TIMEOUT = 8 # seconds
CSFLOAT_TIMEOUT = 8 # seconds
SKINBID_TIMEOUT_PAGE = 4 # seconds
RATIO_MIN = 1.08
PRICE_MIN = 27 # CHANGE also in config specific urls e.g. &pricegt=703


def sleep_random(time):
    return random.randint(time*66, time*88)/100


# read json file
def read_json_file(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


# save json file
def save_json_file(json_file, data):
    with open(json_file, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False)


# calc days trade ban
def trade_ban_days(end_lock_datetime):
    current_date = datetime.now()
    end_lock_datetime = datetime.strptime(end_lock_datetime, '%Y-%m-%d %H:%M:%S')
    difference = end_lock_datetime - current_date
    days_difference = difference.days
    return days_difference
