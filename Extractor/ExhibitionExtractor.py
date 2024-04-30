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

        print(href+": "+str(is_exhibition))

    #list comprehension for the code above, to be implemented later
    #exhibitions = [href for href in site_hrefs if lr.predict_url(model, vectorizer, href)]

    return exhibitions


    #This function will extract all exhibition urls from the exhibition listing
    return

def scrape_exhibiton_details():
    #This function extract all info from the individual exhibition page
    return -1

get_exhibition_urls('https://www.southbankcentre.co.uk/whats-on')
#get_exhibition_urls('https://www.lissongallery.com/exhibitions')