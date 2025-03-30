from dotenv import load_dotenv
import os

load_dotenv()

CSFLOAT_API_URL = "https://csfloat.com/api/v1/listings?limit=50&sort_by=most_recent"

CSFLOAT_HEADERS = {
    'Authorization': os.getenv('CSFLOAT_API_KEY')
}

CSFLOAT_LISTING_URL = "https://csfloat.com/item/"