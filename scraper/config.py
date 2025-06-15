from dotenv import load_dotenv
import os
from pathlib import Path

# 1. Load parent .env from project root
root_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(root_env_path)

# 2. Load local .env.local if not in production
if os.getenv("DOCKER_ENV") != "production":
    local_env_path = Path(__file__).parent / ".env.local"
    load_dotenv(local_env_path, override=True)

STEAM_ICON_URL = "https://steamcommunity-a.akamaihd.net/economy/image/"

SKINS_RARITIES = {
    1: "Consumer Grade",
    2: "Industrial Grade",
    3: "Mil-Spec Grade",
    4: "Restricted",
    5: "Classified",
    6: "Covert",
    7: "Contraband"
}

# Scraper configuration - CSFLOAT
CSFLOAT_API_KEY = os.getenv("CSFLOAT_API_KEY")
CSFLOAT_HEADERS = {
    'Authorization': CSFLOAT_API_KEY
}

CSFLOAT_MARKETPLACE = "CSFLOAT" # Marketplace name
CSFLOAT_LIMIT = 50 # Number of listings to scrape at once (maximum)
CSFLOAT_API_URL = f"https://csfloat.com/api/v1/listings?limit={CSFLOAT_LIMIT}&sort_by=most_recent" # API URL for CSFLOAT newest listings
CSFLOAT_LISTING_URL = "https://csfloat.com/item/" # Base URL for CSFLOAT listings
CSFLOAT_SCRAPE_INTERVAL = 31  # seconds
CSFLOAT_JSON_KEYWORD = "data"

# Scraper configuration - SKINPORT
SKINPORT_MARKETPLACE = "SKINPORT" # Marketplace name
SKINPORT_API_URL = "https://skinport.com/api/browse/730?sort=date&order=desc"
SKINPORT_LISTING_URL = "https://skinport.com/item/" # Base URL for SKINPORT listings
SKINPORT_LIMIT = 50 # Number of listings to scrape at once (maximum)
SKINPORT_SCRAPE_INTERVAL = 21  # seconds
SKINPORT_JSON_KEYWORD = "sales"

# Scraper configuration - SKINBID
SKINBID_API_KEY = os.getenv("SKINBID_API_KEY")
SKINBID_HEADERS = {
    'Authorization': SKINBID_API_KEY
}

SKINBID_MARKETPLACE = "SKINBID" # Marketplace name
SKINBID_LIMIT = 120 # Number of listings to scrape at once (maximum)
SKINBID_API_URL = f"https://api.skinbid.com/api/search/auctions?sort=created%23desc&sellType=fixed_price&take={SKINBID_LIMIT}&skip=0&currency=EUR" # API URL for SKINBID newest listings
SKINBID_LISTING_URL = "https://skinbid.com/listing/" # Base URL for SKINBID listings
SKINBID_SCRAPE_INTERVAL = 26  # seconds
SKINBID_JSON_KEYWORD = "items"

# Scraper configuration - DMarket
DMARKET_MARKETPLACE = "DMARKET" # Marketplace name
DMARKET_LIMIT = 100 # Number of listings to scrape at once (maximum)
DMARKET_API_URL = f"https://api.dmarket.com/exchange/v1/market/items?side=market&orderBy=updated&orderDir=desc&title=&priceFrom=0&priceTo=0&treeFilters=&gameId=a8db&types=dmarket&myFavorites=false&cursor=&limit={DMARKET_LIMIT}&currency=USD&platform=browser&isLoggedIn=false"
DMARKET_LISTING_URL = "https://dmarket.com/ingame-items/item-list/csgo-skins?userOfferId=" # Base URL for DMarket listings
DMARKET_SCRAPE_INTERVAL = 26  # seconds
DMARKET_JSON_KEYWORD = "objects"

# Backend API configuration
BACKEND_API_URL = os.getenv("BACKEND_API_URL")

# Logging configuration
CACHE_FILE = "data/"
LOGS_FILE = "logs/"