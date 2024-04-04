API_HEADERS_SKINPORT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'referer': 'https://skinport.com/pl/market?sort=date&order=desc',
    'Cookie': 'i18n=pl; connect.sid=s%3AQwzwmFXPhGxD_BwLMAXZIIs94cjE-C-_.1OG2reSG1lFtUafWkp4LzSjrP%2FI0iW71lksZNjFTYpc; __cf_bm=MYPP6L5YgqYqueUvAl_KhEyw.PLJxSA2BJqnv09wtk8-1712065537-1.0.1.1-Y8LjhzsvpiN0QbiqzekKyPgJu6DtI4gJLLA_XNnuzNPDeCB31Ut3.37EuZOT1IVgyALJYD7EpdufC67YdDoxQA; _csrf=8FHMYrhFcIwKbPkebjhqsIpR; scid=eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiQTE5MktXIn0.anFeuLC4ZB8ta9Sd419s9NMgHKD8oLPDDYojRezliHtP5MqEFV3a1w.jtYmbMMXg9znXa-TV8BV6Q.2T19ild-WiqFenh4EHCGLLkVQ2NXRZiwn2xxUiX1mrRNPW21xDgGd62_QMY9Nd_C_Jj5dEP5UZ4iX061D2mVRjDxCBOS8ee0LpOuAoyolNHGrNft6m_uXEZTfPbleCWH886i8ZCppXNOhS-NZdRRy6HTgKrqG5qAt2Gq0_kfgRXxLTAhiIXkL_g9BNE4ZLuyAU--JHiU3Za5-1_xJmkU5ka8TianVLxNNBaWLUqRyeC0ztXCVrMXeh7vLBBZbhlNa-rbHy_U0RSmKaEXd1duVYsFBPh-LeMC9K-zCDrOMP68WIAc6Dt2Fpg68BjsuZNm6vVuq39uCcU6_y7_LKvAXhsysj2EtfYdhD0pG8Y0EnOcX7-bRRvjHuNA08fYhsWh_QR-zDlkzQv6915LRboA74Hd6q5bl9O2XLB5Sb2xh5Vv-87SI0DCj1rBNyT_vg9dDO1Gt_XruFeFmesMuoMLP8l1NtYP_vGO_crKYr7WiVulyWofSrCP0_rhsa1e5s7565AWenuddZsvsPm6r2VH_dys5w7GUQTF6sbRLHP6EFWt6e-7HzAPkowPxkA2HX89r3YwVStKqczvkvA9PWn-6rusR5QyUyFRPHTSEr8mAYbp0GKsCPrWdwVw2J8jprDZrmmXBOvKHKAucVc0XeL42H_FPfwGqb1HHvL6b0xA_prqJSpb-EFaR_4JVZS95ptG.3JsDhu9hXmLFp1xwsg9KUw; cf_clearance=_TBfnXRPWofOtHaR7SlvY3eOXroaJfyCbYrxHskKjVA-1712065537-1.0.1.1-Cnwa20h_keVMYXJedItTFbR1HKKEYhqACmIXCZbwuNYGftW9bRcJWZWlKCuKsnSJvLRnQf.PGr.sq2IGOMPdMA'
}



def url_skinport_newest(i):
    return f"https://skinport.com/api/browse/730?sort=date&order=desc&skip={i}"

URL_SKINPORT_NEWEST = "https://skinport.com/api/browse/730?sort=date&order=desc"

def url_skinport_rabat(i):
    return f"https://skinport.com/api/browse/730?sort=percent&order=desc&skip={i}"

URL_SKINPORT_RABAT = "https://skinport.com/api/browse/730?sort=percent&order=desc"

class SkinportOfferInfo:
    def __init__(
        self,
        sale_id: int,
        item_full_name: str,
        item_name: str,
        stattrak: bool,
        sale_price: float,
        sale_cur: str,
        sale_price_pln: float,
        sale_status: str,
        wear: float,
        exterior: str,
        rarity: str,
        item_collection: str,
        item_category: str,
        souvenir: bool,
        stickers: int,
        pattern: int,
        finish: int,
        inspect_link: str,
        custom_name: str,
        weapon_name: str,
        url_slug: str,
        trade_banned: bool,
        trade_ban_end: str,
        scrape_time: str,
        marketplace: str,
        last_update: str,
    ) -> None:
        self.sale_id: sale_id
        self.item_full_name: item_full_name
        self.item_name: item_name
        self.stattrak: stattrak
        self.sale_price: sale_price
        self.sale_cur: sale_cur
        self.sale_price_pln: sale_price_pln
        self.sale_status: sale_status
        self.wear: wear
        self.exterior: exterior
        self.rarity: rarity
        self.item_collection: item_collection
        self.item_category: item_category
        self.souvenir: souvenir
        self.stickers: stickers
        self.pattern: pattern
        self.finish: finish
        self.inspect_link: inspect_link
        self.custom_name: custom_name
        self.weapon_name: weapon_name
        self.url_slug: url_slug
        self.trade_banned: trade_banned
        self.trade_ban_end: trade_ban_end
        self.scrape_time: scrape_time
        self.marketplace: marketplace
        self.last_update: last_update