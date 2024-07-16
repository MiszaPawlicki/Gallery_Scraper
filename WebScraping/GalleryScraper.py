from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import json
from urllib.parse import urlparse
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import ML.Exhibition_Identification.DecisionTree as dt


# Load the Chrome driver once
def load_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (without opening browser window)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver


def fetch_html_content(url, driver):
    driver.get(url)
    time.sleep(5)  # Adjust as needed based on the page load time
    html_content = driver.page_source
    return html_content


def parse_html(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
    except Exception as e:
        print("Error parsing HTML:", str(e))
        return None


def scrape_hrefs(url, driver):
    html_content = fetch_html_content(url, driver)
    if html_content:
        soup = parse_html(html_content)
        if soup:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

            hrefs = []
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    if href.startswith(('http://', 'https://', 'www.')):
                        hrefs.append(href)
                    else:
                        if href.startswith('/'):
                            hrefs.append(base_url + href)
                        else:
                            hrefs.append(base_url + '/' + href)
            unique_hrefs = list(set(hrefs))
            return unique_hrefs
    return None


def get_exhibition_urls(whats_on_url, driver):
    site_hrefs = scrape_hrefs(whats_on_url, driver)
    exhibitions = []

    for href in site_hrefs:
        is_exhibition = dt.predict_url(href)
        if is_exhibition:
            exhibitions.append(href)

    unique_exhibitions = list(set(exhibitions))
    return unique_exhibitions


def load_selectors(json_path):
    with open(json_path, 'r') as file:
        selectors = json.load(file)
    return selectors


def extract_data(url, soup, selectors):
    data = {}
    base_url = "{0.scheme}://{0.netloc}".format(urlparse(url))
    data['url'] = url
    if base_url in selectors:
        css_selectors = selectors[base_url]
        for key, selector in css_selectors.items():
            element = soup.select_one(selector)
            if key == 'image' and element:
                data[key] = element.get('src', None)
            else:
                data[key] = element.get_text(strip=True) if element else None
    else:
        print(f"No selectors found for base URL: {base_url}")

    return data


def get_all_exhibition_details(whats_on_url, selectors, driver):
    exhibition_urls = get_exhibition_urls(whats_on_url, driver)
    all_details = []

    for url in exhibition_urls:
        try:
            html_content = fetch_html_content(url, driver)
            soup = parse_html(html_content)
            details = extract_data(url, soup, selectors)
            print(details)
            all_details.append(details)
        except Exception as e:
            print(f"Failed to process URL {url}: {str(e)}")

    return all_details


def main():
    selectors = load_selectors(
        r'C:\Users\misza\OneDrive\Documents\Work\Personal Projects\Gallery Scraper\ML\Page Detail Extraction\selectors.json')
    driver = load_chrome_driver()
    try:
        all_details = get_all_exhibition_details(
            'https://www.tate.org.uk/whats-on?date_range=from_now&event_type=exhibition&gallery_group=tate-britain&gallery_group=tate-modern',
            selectors, driver)
        print("All details:", all_details)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
