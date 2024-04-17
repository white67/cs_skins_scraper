from discord_webhook import DiscordWebhook, DiscordEmbed
from config.config import *
from config.config_buff import *

def send_webhook_skinport(item_name, sale_price, buff_price, price_ratio, offer_url, icon_url, trade_lock, wear, goods_id):
        
    price_ratio = round(price_ratio*100-100,2)
    if type(wear) == float:
        wear = round(wear,5)
        
    webhook = DiscordWebhook(url=WEBHOOK_URL, rate_limit_retry=True)
    
    # create embed object for webhook
    embed = DiscordEmbed(
        title=item_name,
        url=offer_url,
        color="fca903"
    )
    
    # set thumbnail
    embed.set_thumbnail(url=icon_url)
    
    # set timestamp (default is now) accepted types are int, float and datetime
    embed.set_timestamp()
    
    # set footer
    if trade_lock == 0:
        embed.set_footer(text=f"No trade ban | {wear}")
    else:
        embed.set_footer(text=f"{trade_lock} days | {wear}")
    
    embed.add_embed_field(name="Sale price", value=f"{sale_price}zł")
    embed.add_embed_field(name="Buff price", value=f"{buff_price}zł")
    embed.add_embed_field(name="Ratio", value=f"{price_ratio}%")
    embed.add_embed_field(name="Buff link", value=buff_item_direct_link(goods_id))

    # add embed object to webhook
    webhook.add_embed(embed)
    
    response = webhook.execute()