#from selenium.webdriver.chrome.service import Service as ChromeService
#from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def load_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (without opening browser window)
    driver = webdriver.Chrome(options=options) # Include this as a param if driver not installed: service=ChromeService(ChromeDriverManager().install())
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
            hrefs = [link.get('href') for link in soup.find_all('a')]
            return hrefs
    return None

def get_exhibition_listing():
    # This function will locate the page which contains all exhibition listings
    return -1

def get_exhibition_urls():
    # This function will extract all exhibition urls from the exhibition listing
    return -1

def scrape_exhibition_details():
    # This function extract all info from the individual exhibition page
    return -1

# Example usage
def main():
    # Test the scrape_hrefs function
    url = 'https://example.com'
    hrefs = scrape_hrefs(url)
    if hrefs:
        print(hrefs)
    else:
        print("No hrefs found.")


if __name__ == "__main__":
    main()