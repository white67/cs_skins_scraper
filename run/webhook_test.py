from discord_webhook import DiscordWebhook, DiscordEmbed

WEBHOOK_URL = ""

def send_webhook():
    
    item_name = "★ Sport Gloves | Pandora's Box (Battle-Scarred)"
    sale_price = 7194.02
    buff_price = 8139.47
    price_ratio = round(buff_price/sale_price*100-100,2)
    wear = 0.77901244
    trade_lock = 6
    offer_url = "https://skinport.com/pl/item/sport-gloves-pandora-s-box-battle-scarred/42444412"
    icon_url = "https://market.fp.ps.netease.com/file/65f88f6ea716fdc4c52ddab9adNx6LCj05"
        
    webhook = DiscordWebhook(url=WEBHOOK_URL, rate_limit_retry=True)
    
    # create embed object for webhook
    embed = DiscordEmbed(
        title=item_name,
        url=offer_url,
        color="fca903"
    )
    
    # set image
    # embed.set_image(url=icon_url)
    
    # set thumbnail
    embed.set_thumbnail(url=icon_url)
    
    # set timestamp (default is now) accepted types are int, float and datetime
    embed.set_timestamp()
    
    # set footer
    embed.set_footer(text=f"{trade_lock} days | {wear}")
    
    embed.add_embed_field(name="Sale price", value=f"{sale_price}zł")
    embed.add_embed_field(name="Buff price", value=f"{buff_price}zł")
    embed.add_embed_field(name="Ratio", value=f"{price_ratio}%")

    # add embed object to webhook
    webhook.add_embed(embed)
    
    response = webhook.execute()

send_webhook()