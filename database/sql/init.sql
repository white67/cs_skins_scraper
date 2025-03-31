CREATE DATABASE scraper_db;

-- Create the listings table if it doesn't exist
CREATE TABLE IF NOT EXISTS listings (
    id SERIAL PRIMARY KEY,
    item_name TEXT NOT NULL,
    market_hash_name TEXT NOT NULL,
    item_type TEXT NOT NULL,
    item_type_category TEXT,
    def_index INT,
    paint_index INT,
    paint_seed INT,
    float_value FLOAT,
    icon_url TEXT NOT NULL,
    is_stattrak BOOLEAN DEFAULT FALSE,
    is_souvenir BOOLEAN DEFAULT FALSE,
    rarity TEXT,
    wear TEXT,
    tradable BOOLEAN NOT NULL,
    trade_ban_days INT,
    inspect_link TEXT,
    item_description TEXT,
    item_collection TEXT,
    price FLOAT NOT NULL,
    price_currency TEXT NOT NULL,
    listing_id BIGINT NOT NULL,
    listing_url TEXT NOT NULL,
    listing_timestamp BIGINT NOT NULL,
    marketplace TEXT NOT NULL
);