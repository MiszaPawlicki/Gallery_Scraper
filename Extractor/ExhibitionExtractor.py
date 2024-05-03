import WebScraping.GalleryScraper as scraper
import ML.LogisticalRegression as lr
def get_exhibition_urls(url):

    model, vectorizer = lr.load_model()
    site_hrefs = scraper.scrape_hrefs(url)
    exhibitions = []

    for href in site_hrefs:
        is_exhibition = lr.predict_url(model, vectorizer, href)
        if is_exhibition:
            exhibitions.append(href)
            print(href)

    return exhibitions

def scrape_exhibiton_details():
    #This function extract all info from the individual exhibition page
    return -1


def test():
    exhibitions = [
        'https://www.southbankcentre.co.uk/whats-on',
        'https://www.lissongallery.com/exhibitions',
        'https://www.tate.org.uk/whats-on',
        'https://www.barbican.org.uk/whats-on/art-design',
        'https://www.saatchigallery.com/whats-on',
        'https://www.somersethouse.org.uk/whats-on',
        'https://www.npg.org.uk/whatson/events-calendar',
        'https://www.dulwichpicturegallery.org.uk/whats-on/exhibitions/',
        'https://camdenartcentre.org/whats-on/in-the-building/exhibitions'

    ]


    all_exhibitions = []
    for url in exhibitions:
        found_exhibitions = get_exhibition_urls(url)
        if found_exhibitions:
            for e in found_exhibitions:
                all_exhibitions.append(e)

    for e in  all_exhibitions:
        print(e)

