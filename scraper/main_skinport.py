import signal
import sys
import os
from scrapers.skinport_scraper import SkinportScraper
from config import SKINPORT_MARKETPLACE

def signal_handler(sig, frame):
    print(f"\nStopping {SKINPORT_MARKETPLACE} scraper...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    scraper = SkinportScraper()
    print(f"Starting {SKINPORT_MARKETPLACE} scraper (PID: {os.getpid()})")
    
    try:
        scraper.run()
    except KeyboardInterrupt:
        print("\nScraper stopped by user")
    except Exception as e:
        print(f"Critical error: {str(e)}")
        sys.exit(1)
