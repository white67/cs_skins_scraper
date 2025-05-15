import threading
from scraper.scrapers.dmarket_scaper import DMARKETScraper
import time

if __name__ == "__main__":
    
    # Start the scraper in a separate thread
    scraper = DMARKETScraper()

    threading.Thread(
        target=scraper.run_scraper(),
        args=(scraper,),
        daemon=True
    ).start()

    threading.Event().wait()
    
    try:
        while True:
            time.sleep(1)  # lower CPU usage
    except KeyboardInterrupt:
        print("Stopping scraper...")