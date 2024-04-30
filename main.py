from WebScraping.GalleryScraper import Scraper

scraper = Scraper('https://bbc.co.uk')
print(scraper.scrape('https://bbc.co.uk'))