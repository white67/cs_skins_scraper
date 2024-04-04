import requests #dependency

WEBHOOK_SKINPORT_URL = "https://discord.com/api/webhooks/1225573919310876712/eyzZpUgGesgnkeBAudZVE4tjtd-TLF0zIt5a1wvT_cyQRXTDEZodYRjLg8jDrH4Pm9v3" #webhook url, from here: https://i.imgur.com/f9XnAew.png

def send_webhook_skinport(item_name, sale_price, buff_price, price_ratio, sale_link, img):
        
    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data = {
        "content" : "Found new profitable offer!"
    }

    #leave this out if you dont want an embed
    #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data["embeds"] = [
        {
            "description" : f"Sale price: {sale_price} pln Buff price: {buff_price} Ratio: {price_ratio}",
            "title" : f"{item_name}",
            # "url": sale_link,
            # "thumbnail": img
        }
    ]
    headers = {
        "Content-Type": "application/json"
    }

    result = requests.post(WEBHOOK_SKINPORT_URL, json = data, headers=headers)

    print("################################# sending webhook")
    
    if 200 <= result.status_code < 300:
        print(f"Webhook sent {result.status_code}")
    else:
        print(f"Not sent with {result.status_code}, response:\n{result.json()}")