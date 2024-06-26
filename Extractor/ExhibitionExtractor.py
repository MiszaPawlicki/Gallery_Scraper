import WebScraping.GalleryScraper as scraper
import ML.DecisionTree as dt


def get_exhibition_urls(url):
    site_hrefs = scraper.scrape_hrefs(url)
    exhibitions = []

    for href in site_hrefs:
        is_exhibition = dt.predict_url(href)
        if is_exhibition:
            exhibitions.append(href)

    unique_exhibitions = list(set(exhibitions))

    return unique_exhibitions


def scrape_exhibition_details(url):
    found_exhibitions = get_exhibition_urls(url)
    exhibition_list = []
    if found_exhibitions:
        for e in found_exhibitions:
            print(e)
            exhibition_list.append(e)

    if exhibition_list:
        return exhibition_list

    return -1

def main():
    scrape_exhibition_details('https://www.southbankcentre.co.uk/whats-on?type=art-exhibitions')


if __name__ == "__main__":
    main()
