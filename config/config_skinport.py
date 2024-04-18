URL_SKINPORT_NEWEST = "https://skinport.com/api/browse/730?sort=date&order=desc"
URL_SKINPORT_RABAT = "https://skinport.com/api/browse/730?sort=percent&order=desc"

def skinport_sale_link(sale_id, url_slug_name):
    return f"https://skinport.com/pl/item/{url_slug_name}/{sale_id}"


def url_skinport_newest(i):
    return f"https://skinport.com/api/browse/730?sort=date&order=desc&pricegt=703&skip={i}"


def url_skinport_rabat(i):
    return f"https://skinport.com/api/browse/730?sort=percent&order=desc&pricegt=703&skip={i}"


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