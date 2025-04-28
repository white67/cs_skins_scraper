from dotenv import load_dotenv
import os

load_dotenv()

# Scraper configuration - CSFLOAT
CSFLOAT_HEADERS = {
    'Authorization': os.getenv('CSFLOAT_API_KEY')
}
CSFLOAT_MARKETPLACE = "CSFLOAT" # Marketplace name
CSFLOAT_API_URL = "https://csfloat.com/api/v1/listings?limit=50&sort_by=most_recent" # API URL for CSFLOAT newest listings
CSFLOAT_LISTING_URL = "https://csfloat.com/item/" # Base URL for CSFLOAT listings
CSFLOAT_LIMIT = 50 # Number of listings to scrape at once (maximum)
CSFLOAT_SCRAPE_INTERVAL = 44  # seconds

# Scraper configuration - SKINPORT
SKINPORT_MARKETPLACE = "SKINPORT" # Marketplace name
SKINPORT_API_URL = "https://skinport.com/api/browse/730?sort=date&order=desc"
SKINPORT_LISTING_URL = "https://skinport.com/item/" # Base URL for SKINPORT listings
SKINPORT_LIMIT = 50 # Number of listings to scrape at once (maximum)
SKINPORT_SCRAPE_INTERVAL = 21  # seconds

# Backend API configuration
BACKEND_API_URL = "http://localhost:8080/api/listings"

# Logging configuration
CACHE_FILE = "scraper/data/"
LOGS_FILE = "scraper/logs/"