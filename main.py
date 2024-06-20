import Extractor.ExhibitionExtractor as extractor
import WebScraping.GalleryScraper as scraper
import Database.Database as db

# 'https://www.southbankcentre.co.uk/whats-on?type=art-exhibitions',
# 'https://www.lissongallery.com/exhibitions',
# 'https://www.tate.org.uk/whats-on?date_range=from_now&gallery_group=tate-britain&gallery_group=tate-modern',
# 'https://www.barbican.org.uk/whats-on/art-design',
# 'https://www.saatchigallery.com/whats-on',
# 'https://www.somersethouse.org.uk/whats-on',
# 'https://www.npg.org.uk/whatson/events-calendar',
# 'https://www.dulwichpicturegallery.org.uk/whats-on/exhibitions/',
# 'https://camdenartcentre.org/whats-on/in-the-building/exhibitions'

urls = [

    'https://www.tate.org.uk/whats-on?date_range=from_now&gallery_group=tate-britain&gallery_group=tate-modern',
    'https://www.barbican.org.uk/whats-on/art-design',
    'https://www.saatchigallery.com/whats-on',
    'https://www.somersethouse.org.uk/whats-on',
    'https://www.southbankcentre.co.uk/whats-on?type=art-exhibitions'

]

db.create_table()
for url in urls:

    galleries = extractor.scrape_exhibition_details(url)

    gallery_details = []

    for gallery_url in galleries:
        details = scraper.scrape_exhibition_details(gallery_url)
        if details:
            print(details)

            db.insert_exhibition(details)
