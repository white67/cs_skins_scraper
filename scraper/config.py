from dotenv import load_dotenv
import os
from pathlib import Path

def load_csfloat_headers():
    """
    Load environment variables from .env file.
    """
    load_dotenv(override=True)  # overrides existing variables
    return os.getenv('CSFLOAT_API_KEY')

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
CSFLOAT_HEADERS = {
    'Authorization': load_csfloat_headers()
}
CSFLOAT_MARKETPLACE = "CSFLOAT" # Marketplace name
CSFLOAT_API_URL = "https://csfloat.com/api/v1/listings?limit=50&sort_by=most_recent" # API URL for CSFLOAT newest listings
CSFLOAT_LISTING_URL = "https://csfloat.com/item/" # Base URL for CSFLOAT listings
CSFLOAT_LIMIT = 50 # Number of listings to scrape at once (maximum)
CSFLOAT_SCRAPE_INTERVAL = 31  # seconds
CSFLOAT_JSON_KEYWORD = "data"

# Scraper configuration - SKINPORT
SKINPORT_MARKETPLACE = "SKINPORT" # Marketplace name
SKINPORT_API_URL = "https://skinport.com/api/browse/730?sort=date&order=desc"
SKINPORT_LISTING_URL = "https://skinport.com/item/" # Base URL for SKINPORT listings
SKINPORT_LIMIT = 50 # Number of listings to scrape at once (maximum)
SKINPORT_SCRAPE_INTERVAL = 21  # seconds

# Scraper configuration - SKINBID
SKINBID_HEADERS = {
    'Authorization': os.getenv('SKINBID_API_KEY')
}
SKINBID_MARKETPLACE = "SKINBID" # Marketplace name
SKINBID_API_URL = "https://api.skinbid.com/api/search/auctions?sort=created%23desc&sellType=fixed_price&take=120&skip=0&currency=EUR" # API URL for SKINBID newest listings
SKINBID_LISTING_URL = "https://skinbid.com/listing/" # Base URL for SKINBID listings
SKINBID_LIMIT = 120 # Number of listings to scrape at once (maximum)
SKINBID_SCRAPE_INTERVAL = 26  # seconds
SKINBID_JSON_KEYWORD = "items"

# Scraper configuration - DMarket
DMARKET_MARKETPLACE = "DMARKET" # Marketplace name
DMARKET_API_URL = "https://api.dmarket.com/exchange/v1/market/items?side=market&orderBy=updated&orderDir=desc&title=&priceFrom=0&priceTo=0&treeFilters=&gameId=a8db&types=dmarket&myFavorites=false&cursor=&limit=100&currency=USD&platform=browser&isLoggedIn=false"
DMARKET_LISTING_URL = "https://dmarket.com/ingame-items/item-list/csgo-skins?userOfferId=" # Base URL for DMarket listings
DMARKET_LIMIT = 100 # Number of listings to scrape at once (maximum)
DMARKET_SCRAPE_INTERVAL = 26  # seconds
DMARKET_JSON_KEYWORD = "objects"

# Backend API configuration
BACKEND_API_URL = "http://localhost:8080/api/listings"

# Logging configuration
CACHE_FILE = "scraper/data/"
LOGS_FILE = "scraper/logs/"