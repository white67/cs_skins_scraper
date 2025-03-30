# test one time scrape
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scrapers.csfloat_scraper as csfloat_scraper

results = csfloat_scraper.CSFLOATScraper().scrape()

print(results[0])

print("xd")