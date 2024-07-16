import WebScraping.GalleryScraper as scraper
import Database.Database as db

urls = [
#    "https://www.southbankcentre.co.uk/whats-on?type=art-exhibitions",
#    "https://www.lissongallery.com/exhibitions",
    "https://www.tate.org.uk/whats-on?date_range=from_now&event_type=exhibition&gallery_group=tate-britain&gallery_group=tate-modern",
#    "https://www.barbican.org.uk/whats-on/art-design",
#    "https://www.saatchigallery.com/whats-on",
#    "https://www.saatchigallery.com/whats-on/upcoming",
#    "https://www.somersethouse.org.uk/whats-on",
#    "https://www.npg.org.uk/whatson/events-calendar",
#    "https://www.dulwichpicturegallery.org.uk/whats-on/exhibitions/",
#    "https://camdenartcentre.org/whats-on/in-the-building/exhibitions"
]

# TODO redo the refactor
db.create_table()
for url in urls:
    selectors = scraper.load_selectors(
        r'C:\Users\misza\OneDrive\Documents\Work\Personal Projects\Gallery Scraper\ML\Page Detail Extraction\selectors.json')
    driver = scraper.load_chrome_driver()
    exhibitions = scraper.get_all_exhibition_details(url, selectors, driver)
    db.insert_exhibitions(exhibitions)