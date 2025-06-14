import os
import signal
import sys
from scrapers.skinbid_scraper import SkinBidScraper
from config import SKINBID_MARKETPLACE

def signal_handler(sig, frame):
    print(f"\nStopping {SKINBID_MARKETPLACE} scraper...")
    sys.exit(0)

if __name__ == "__main__":
    # Register Ctrl+C handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Initialize and run scraper
    scraper = SkinBidScraper()
    print(f"Starting {SKINBID_MARKETPLACE} scraper (PID: {os.getpid()})")
    
    try:
        scraper.run()
    except KeyboardInterrupt:
        print("\nScraper stopped by user")
    except Exception as e:
        print(f"Critical error: {str(e)}")
        sys.exit(1)