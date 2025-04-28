import os
import time
import random
import requests
import psycopg2

from dotenv import load_dotenv

from scraper.models.base_model import Listing

# Load environment variables from .env file
load_dotenv()

class BaseScraper:
    """
    Base class for scrapers.
    """
    def __init__(self, marketplace_name: str, api_url: str):
        self.marketplace_name = marketplace_name
        self.api_url = api_url

    def fetch_data(self, endpoint, headers={}):
        """
        Fetch data from the API endpoint.
        """
        
        url = f"{self.api_url}{endpoint}"
        print(f"Fetching data from {url}")
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    
    def sleep_random(self):
        """
        Sleep for a random time between 8 and 12 seconds.
        """
        time.sleep(random.uniform(8, 12))
    
    def insert_listing_to_db(self, listing: Listing):
        """
        Inserts a single listing into the PostgreSQL database.
        """
        
        try:
            # Load environment variables
            DB_HOST = os.getenv("DB_HOST")
            DB_PORT = os.getenv("DB_PORT")
            DB_NAME = os.getenv("DB_NAME")
            DB_USER = os.getenv("POSTGRES_USER")
            DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
            
            # Connect to PostgreSQL database
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            cursor = conn.cursor()

            # Prepare the insert query
            insert_query = listing.generate_insert_query()
            
            # Prepare the data to insert
            data = listing.to_db_tuple()
            
            # Execute the query
            cursor.execute(insert_query, data)

            # Commit the transaction
            conn.commit()

            print(f"Inserted listing {listing.item_name} into database.")

        except Exception as e:
            print(f"Error inserting listing to database: {e}")
        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()

    def insert_new_listings_to_db(self, new_listings):
        """
        Inserts a list of new listings into the database.
        """
        for listing in new_listings:
            self.insert_listing_to_db(listing)