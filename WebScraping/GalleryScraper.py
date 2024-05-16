# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import WebScraping.GalleryScraper as scraper
import ML.RandomForrest as rf


# TODO refactor such that driver is loaded once
# TODO refactor to separate NLP from web scraping, this would be best practise
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

    def getBio():
        # not sure how to do
        return -1

    def getPrice():
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

        # Extract numerical values from price elements
        prices = []
        free_occurrences = []

        for element in price_elements:
            text = element.get_text(strip=True)

            # Check for "free" keyword
            if re.search(r'\bfree\b', text, re.IGNORECASE):
                free_occurrences.append(text)

            # Find prices following the pound symbol
            price_matches = re.findall(r'£\s*(\d+(\.\d+)?)', text)
            for price in price_matches:
                try:
                    prices.append(float(price[0]))  # price[0] because re.findall returns tuples
                except ValueError:
                    continue

        # Determine minimum and maximum prices
        if free_occurrences and not prices:
            min_price = 'free'
            max_price = 'free'
        elif prices:
            min_price = min(prices) if not free_occurrences else 'free'
            max_price = max(prices)
        else:
            min_price = 'Not listed'
            max_price = 'Not listed'

        return min_price, max_price

    def getImages():
        # TODO this is flakey, should have additional checks

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

        for element in postcode_elements:
            text = element.get_text().strip()

            # Regular expression pattern to match UK postcodes in various formats
            postcode_pattern = r'[A-Z]{1,2}\d{1,2}[A-Z]?\s*\d[A-Z]{2}'

            # Find the first match of postcode pattern in the text
            postcode_match = re.search(postcode_pattern, text)
            if postcode_match:
                return postcode_match.group()

        return None

    return {'Title': getTitle(), 'Bio': getBio(), 'Price': getPrice(), 'Images': getImages(), 'Location': getLocation()}


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
