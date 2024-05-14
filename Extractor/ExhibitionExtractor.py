import WebScraping.GalleryScraper as scraper
import ML.RandomForrest as rf
def get_exhibition_urls(url):

    site_hrefs = scraper.scrape_hrefs(url)
    exhibitions = []

    for href in site_hrefs:
        is_exhibition = rf.predict_url(href)
        if is_exhibition:
            exhibitions.append(href)


    unique_exhibitions = list(set(exhibitions))
    return unique_exhibitions

def scrape_exhibiton_details():
    #This function extract all info from the individual exhibition page
    return -1


def test():
    exhibitions = [
        'https://www.southbankcentre.co.uk/whats-on?type=art-exhibitions',
        #'https://www.lissongallery.com/exhibitions',
        #'https://www.tate.org.uk/whats-on?event_type=exhibition',
        #'https://www.barbican.org.uk/whats-on/art-design',
        #'https://www.saatchigallery.com/whats-on',
        #'https://www.somersethouse.org.uk/whats-on',
        #'https://www.npg.org.uk/whatson/events-calendar',
        #'https://www.dulwichpicturegallery.org.uk/whats-on/exhibitions/',
        #'https://camdenartcentre.org/whats-on/in-the-building/exhibitions'

    ]

    for url in exhibitions:
        print('url: ' + url)
        found_exhibitions = get_exhibition_urls(url)
        if found_exhibitions:
            for e in found_exhibitions:
                print(e)



test()