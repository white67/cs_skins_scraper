import threading
from scraper.scrapers.skinport_scraper import SKINPORTScraperWS

if __name__ == "__main__":

    threading.Thread(
        target=SKINPORTScraperWS().start,
        daemon=True
    ).start()

    threading.Event().wait()