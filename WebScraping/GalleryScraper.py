# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import NLP
import WebScraping.GalleryScraper as scraper
import ML.RandomForrest as rf


# TODO refactor such that driver is loaded once
def load_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (without opening browser window)
    driver = webdriver.Chrome(
        options=options)  # Include this as a param if driver not installed: service=ChromeService(ChromeDriverManager().install())
    return driver


def fetch_html_content(url, driver):
    driver.get(url)
    time.sleep(5)
    html_content = driver.page_source
    driver.quit()
    return html_content


def parse_html(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
    except Exception as e:
        print("Error parsing HTML:", str(e))
        return None


def scrape_hrefs(url):
    driver = load_chrome_driver()
    html_content = fetch_html_content(url, driver)
    if html_content:
        soup = parse_html(html_content)
        if soup:
            if url.startswith("http://") or url.startswith("https://"):
                base_url = "https://" + url.split('//', 1)[1].split('/', 1)[0]  # Extracting the base URL
            elif url.startswith("http://"):
                base_url = "http://" + url.split('//', 1)[1].split('/', 1)[0]  # Extracting the base URL
            elif url.startswith("www."):
                base_url = url.split('/', 1)[0]  # Extracting the base URL
            else:
                if "//" in url:
                    protocol, rest = url.split('//', 1)
                    base_url = protocol + '//' + rest.split('/', 1)[0]  # Extracting the base URL
                else:
                    base_url = url.split('/', 1)[0]  # Extracting the base URL

            hrefs = []
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    if href.startswith("http://") or href.startswith("https://") or href.startswith("www.") or (
                            href.startswith("//") and href.split("//", 1)[1].startswith(base_url)):
                        hrefs.append(href)
                    else:
                        if href.startswith("/"):
                            hrefs.append(base_url + href)
                        else:
                            hrefs.append(base_url + "/" + href)

            unique_hrefs = list(set(hrefs))
            return unique_hrefs

    return None


def get_exhibition_listing():
    # This function will locate the page which contains all exhibition listings
    return -1


def get_exhibition_urls(whats_on_url):
    site_hrefs = scraper.scrape_hrefs(whats_on_url)
    exhibitions = []

    for href in site_hrefs:
        is_exhibition = rf.predict_url(href)
        if is_exhibition:
            exhibitions.append(href)

    unique_exhibitions = list(set(exhibitions))
    return unique_exhibitions


def scrape_exhibition_details(url):
    driver = load_chrome_driver()
    html_content = fetch_html_content(url, driver)
    soup = parse_html(html_content)

    def getTitle():
        # Find the <h1> element
        title_element = soup.find('h1')

        if title_element:
            # Extract the text of the <h1> element
            title = title_element.text

            # Replace escape characters with spaces
            title = title.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

            return title.strip()
        else:
            return None

    def getDescription():
        # not sure how to do
        return -1

    def getPrices():
        # TODO This is still pulling prices for things such as memberships, need to find way to ignore

        # Find the main content area
        main_content = soup.find('main')
        if not main_content:
            # If no <main> tag is found, fall back to a div with class 'main' or 'content'
            main_content = soup.find('div', class_=re.compile(r'main|content', re.IGNORECASE))

        if not main_content:
            return 'Not listed', 'Not listed'

        # Find all elements within the main content area with class names containing 'price'
        price_elements = main_content.find_all(class_=re.compile(r'price', re.IGNORECASE))

        # Using NLP, find price of the exhibition
        min_price, max_price = NLP.findPrices(price_elements)

        return min_price, max_price

    def getImage():
        # TODO need to find more concrete way of discerning main image
        # TODO needs to append base url if just a path

        # Find the <main> tag
        main_content = soup.find('main')

        if main_content:
            # Find the first image tag within the <main> content
            first_image = main_content.find('img')

            # Extract the src attribute of the first image
            if first_image:
                return first_image.get('src')
            else:
                return None
        else:
            return None

    def getLocation():
        # TODO this is fine as a placeholder but it should really check for elements under the header of location first

        # Find elements containing potential postcode information based on common patterns
        postcode_elements = soup.find_all(['div', 'span', 'p'])

        # Using NLP, find strings that match postcode REGEX
        postcodes = NLP.findLocations(postcode_elements)

        return postcodes



    def getDate():
        # Search in the main content first
        main_tag = soup.find('main')
        if main_tag:
            date_text = search_for_date_in_tag(main_tag)
            if date_text:
                return date_text

        # If not found, search in the rest of the body
        body_tag = soup.find('body')
        if body_tag:
            date_text = search_for_date_in_tag(body_tag)
            if date_text:
                return date_text

        # If still not found, return None
        return None

    def search_for_date_in_tag(tag):
        # List of tags to search for dates
        tags_to_search = ['p', 'div', 'span', 'h2', 'h3', 'h4', 'h5', 'h6', 'time']
        date_pattern = re.compile(
            r'\b(?:(Mon|Tue|Wed|Thu|Fri|Sat|Sun)(?:day)?)?\s*'  # Optional day name
            r'(\d{1,2})(?:st|nd|rd|th)?\s*'  # Day with optional ordinal suffix
            r'(?:(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?:uary|ch|il|e|y|ust|tember|ober|ember)?)\s*'  # Month
            r'(\d{4})?\b'  # Optional year
            r'(?:\s*[-–—]\s*'  # Date range separator: hyphen, en dash, or em dash
            r'(?:(Mon|Tue|Wed|Thu|Fri|Sat|Sun)(?:day)?)?\s*'  # Optional second day name
            r'(\d{1,2})(?:st|nd|rd|th)?\s*'  # Second day with optional ordinal suffix
            r'(?:(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?:uary|ch|il|e|y|ust|tember|ober|ember)?)\s*'  # Second month
            r'(\d{4})?)?'  # Optional second year
            , re.IGNORECASE)

        # Iterate through specified tags and search for dates
        for tag_name in tags_to_search:
            for element in tag.find_all(tag_name):
                text = element.get_text(strip=True)
                if date_pattern.search(text):
                    return text

        return None

    def getGallery():
        return -1;
    # refactor, this is ugly
    min_price, max_price = getPrices()

    return {
        'url': url,
        'title': getTitle(),
        'description': getDescription(),
        'min_price': min_price,
        'max_price': max_price,
        'image': getImage(),
        'location': getLocation()
    }


def get_all_exhibition_details(whats_on_url):
    # this function will eventually return all exhibition details
    exhibition_urls = get_exhibition_urls(whats_on_url)
    for url in exhibition_urls:
        details = scrape_exhibition_details(url)
        print(url)
        print(str(details) + '\n')


# Example usage
def main():
    get_all_exhibition_details('https://www.southbankcentre.co.uk/whats-on?type=art-exhibitions')


if __name__ == "__main__":
    main()
