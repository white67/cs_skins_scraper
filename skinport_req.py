# get current nba odds

import sys
import time
sys.path.append('')
import requests
import json
from datetime import datetime, timedelta, timezone

def write_json_file(json_file, data):
    with open(json_file, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False)


response = requests.get("https://skinport.com/api/browse/730?sort=date&order=desc", headers=api_headers_skinport)


if response.status_code == 200:
    print("Code: 200")
    
    # get all events ids and then parse to api one-by-one
    response = response.json()
    
    write_json_file("xd.json", response)
    
    for item in response["items"]:
        print(item["marketHashName"])
    
elif response.status_code == 404:
        print(f"Code: 404")
else:
    print("Request failed with status code:", response.status_code)
