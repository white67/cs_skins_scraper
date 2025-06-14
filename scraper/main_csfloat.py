import os
import signal
import sys
from scrapers.csfloat_scraper import CSFloatScraper
from config import CSFLOAT_MARKETPLACE

def signal_handler(sig, frame):
    print(f"\nStopping {CSFLOAT_MARKETPLACE} scraper...")
    sys.exit(0)

if __name__ == "__main__":
    # Register Ctrl+C handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Initialize and run scraper
    scraper = CSFloatScraper()
    print(f"Starting {CSFLOAT_MARKETPLACE} scraper (PID: {os.getpid()})")
    
    try:
        scraper.run()
    except KeyboardInterrupt:
        print("\nScraper stopped by user")
    except Exception as e:
        print(f"Critical error: {str(e)}")
        sys.exit(1)