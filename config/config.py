import sys
import random
sys.path.append('')
import requests
import json
from datetime import datetime, timedelta, timezone


WEBHOOK_SKINPORT_URL = "https://discord.com/api/webhooks/1229489855881416734/kjwTZdLTNrw3uqn24nT1XSLWR8eiTn9PKvoRfbmik_PXfx95Ppo2ILxuPkkzigX0d80g"
WEBHOOK_SKINBID_URL = "https://discord.com/api/webhooks/1230577366091301045/BfgUgGxmeE_yPnerW_-YmWKIJo6EgKnsIlNrwdr8YggaDNJO5sQ3FjCyG56mEkc7NenN"
API_HEADERS_SKINPORT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'referer': 'https://skinport.com/pl/market?sort=date&order=desc',
    'Cookie': 'i18n=pl; connect.sid=s%3AQwzwmFXPhGxD_BwLMAXZIIs94cjE-C-_.1OG2reSG1lFtUafWkp4LzSjrP%2FI0iW71lksZNjFTYpc; __cf_bm=MYPP6L5YgqYqueUvAl_KhEyw.PLJxSA2BJqnv09wtk8-1712065537-1.0.1.1-Y8LjhzsvpiN0QbiqzekKyPgJu6DtI4gJLLA_XNnuzNPDeCB31Ut3.37EuZOT1IVgyALJYD7EpdufC67YdDoxQA; _csrf=8FHMYrhFcIwKbPkebjhqsIpR; scid=eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiQTE5MktXIn0.anFeuLC4ZB8ta9Sd419s9NMgHKD8oLPDDYojRezliHtP5MqEFV3a1w.jtYmbMMXg9znXa-TV8BV6Q.2T19ild-WiqFenh4EHCGLLkVQ2NXRZiwn2xxUiX1mrRNPW21xDgGd62_QMY9Nd_C_Jj5dEP5UZ4iX061D2mVRjDxCBOS8ee0LpOuAoyolNHGrNft6m_uXEZTfPbleCWH886i8ZCppXNOhS-NZdRRy6HTgKrqG5qAt2Gq0_kfgRXxLTAhiIXkL_g9BNE4ZLuyAU--JHiU3Za5-1_xJmkU5ka8TianVLxNNBaWLUqRyeC0ztXCVrMXeh7vLBBZbhlNa-rbHy_U0RSmKaEXd1duVYsFBPh-LeMC9K-zCDrOMP68WIAc6Dt2Fpg68BjsuZNm6vVuq39uCcU6_y7_LKvAXhsysj2EtfYdhD0pG8Y0EnOcX7-bRRvjHuNA08fYhsWh_QR-zDlkzQv6915LRboA74Hd6q5bl9O2XLB5Sb2xh5Vv-87SI0DCj1rBNyT_vg9dDO1Gt_XruFeFmesMuoMLP8l1NtYP_vGO_crKYr7WiVulyWofSrCP0_rhsa1e5s7565AWenuddZsvsPm6r2VH_dys5w7GUQTF6sbRLHP6EFWt6e-7HzAPkowPxkA2HX89r3YwVStKqczvkvA9PWn-6rusR5QyUyFRPHTSEr8mAYbp0GKsCPrWdwVw2J8jprDZrmmXBOvKHKAucVc0XeL42H_FPfwGqb1HHvL6b0xA_prqJSpb-EFaR_4JVZS95ptG.3JsDhu9hXmLFp1xwsg9KUw; cf_clearance=_TBfnXRPWofOtHaR7SlvY3eOXroaJfyCbYrxHskKjVA-1712065537-1.0.1.1-Cnwa20h_keVMYXJedItTFbR1HKKEYhqACmIXCZbwuNYGftW9bRcJWZWlKCuKsnSJvLRnQf.PGr.sq2IGOMPdMA'
}
API_HEADERS_SKINBID = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}
API_HEADERS_BUFF = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Cookie': 'Device-Id=BGPsVUlaN0dcDxaXmrqn; Locale-Supported=en; game=csgo; session=1-w92KtZYfBULSJr-VKjMT2kwScEMbCrXLUAGqxES1VaeS2034437484; csrf_token=IjA2ZWMyYTQ1N2I3NjNmNzM5MjE3NjZlMWQ1NGYyYmRlMmU4NWJkODMi.GPB37w.XvLr1zPCo4cc4j1aBwHO-wkxmMs'
}
CNY_PLN = 0.562
API_TIMEOUT = 1 # seconds
SKINPORT_TIMEOUT = 8 # seconds
SKINBID_TIMEOUT = 4 # seconds
RATIO_MIN = 1.09
PRICE_MIN = 27 # CHANGE also in config specific urls e.g. &pricegt=703


def sleep_random(time):
    return random.randint(time*88, time*112)/100


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
