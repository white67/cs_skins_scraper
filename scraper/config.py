import os

CSFLOAT_API_URL = "https://csfloat.com/api/v1/listings?limit=50&sort_by=most_recent"

CSFLOAT_PARAMS = {
    'Authorization': os.getenv('CSFLOAT_API_KEY', 'default_value_if_missing')
}

CSFLOAT_LISTING_URL = "https://csfloat.com/item/"