#from selenium.webdriver.chrome.service import Service as ChromeService
#from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import time

#TODO refactor such that driver is loaded once
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
                    if href.startswith("http://") or href.startswith("https://") or href.startswith("www.") or (href.startswith("//") and href.split("//",1)[1].startswith(base_url)):
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