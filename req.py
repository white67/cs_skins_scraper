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

api_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'referer': 'https://skinport.com/pl/market?sort=date&order=desc',
    'Cookie': 'i18n=pl; connect.sid=s%3AQwzwmFXPhGxD_BwLMAXZIIs94cjE-C-_.1OG2reSG1lFtUafWkp4LzSjrP%2FI0iW71lksZNjFTYpc; __cf_bm=MYPP6L5YgqYqueUvAl_KhEyw.PLJxSA2BJqnv09wtk8-1712065537-1.0.1.1-Y8LjhzsvpiN0QbiqzekKyPgJu6DtI4gJLLA_XNnuzNPDeCB31Ut3.37EuZOT1IVgyALJYD7EpdufC67YdDoxQA; _csrf=8FHMYrhFcIwKbPkebjhqsIpR; scid=eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiQTE5MktXIn0.anFeuLC4ZB8ta9Sd419s9NMgHKD8oLPDDYojRezliHtP5MqEFV3a1w.jtYmbMMXg9znXa-TV8BV6Q.2T19ild-WiqFenh4EHCGLLkVQ2NXRZiwn2xxUiX1mrRNPW21xDgGd62_QMY9Nd_C_Jj5dEP5UZ4iX061D2mVRjDxCBOS8ee0LpOuAoyolNHGrNft6m_uXEZTfPbleCWH886i8ZCppXNOhS-NZdRRy6HTgKrqG5qAt2Gq0_kfgRXxLTAhiIXkL_g9BNE4ZLuyAU--JHiU3Za5-1_xJmkU5ka8TianVLxNNBaWLUqRyeC0ztXCVrMXeh7vLBBZbhlNa-rbHy_U0RSmKaEXd1duVYsFBPh-LeMC9K-zCDrOMP68WIAc6Dt2Fpg68BjsuZNm6vVuq39uCcU6_y7_LKvAXhsysj2EtfYdhD0pG8Y0EnOcX7-bRRvjHuNA08fYhsWh_QR-zDlkzQv6915LRboA74Hd6q5bl9O2XLB5Sb2xh5Vv-87SI0DCj1rBNyT_vg9dDO1Gt_XruFeFmesMuoMLP8l1NtYP_vGO_crKYr7WiVulyWofSrCP0_rhsa1e5s7565AWenuddZsvsPm6r2VH_dys5w7GUQTF6sbRLHP6EFWt6e-7HzAPkowPxkA2HX89r3YwVStKqczvkvA9PWn-6rusR5QyUyFRPHTSEr8mAYbp0GKsCPrWdwVw2J8jprDZrmmXBOvKHKAucVc0XeL42H_FPfwGqb1HHvL6b0xA_prqJSpb-EFaR_4JVZS95ptG.3JsDhu9hXmLFp1xwsg9KUw; cf_clearance=_TBfnXRPWofOtHaR7SlvY3eOXroaJfyCbYrxHskKjVA-1712065537-1.0.1.1-Cnwa20h_keVMYXJedItTFbR1HKKEYhqACmIXCZbwuNYGftW9bRcJWZWlKCuKsnSJvLRnQf.PGr.sq2IGOMPdMA'
}


response = requests.get("https://skinport.com/api/browse/730?sort=date&order=desc&skip=11", headers=api_headers)


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
