import json
import re
import logging

# Configure logging
logging.basicConfig(filename='url_classification.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

url_dict_path = r'C:\Users\misza\OneDrive\Documents\Work\Personal Projects\Gallery Scraper\ML\url_dict.json'

class UrlFeaturizer:
    def __init__(self, url):
        self.base_url, self.path = self.extractPath(url)

    def extractPath(self, url):
        url = re.sub(r'^https?://(?:www\.)?', '', url)
        match = re.match(r'([^/]+)(.*)', url)
        base_url = match.group(1)
        path = match.group(2)
        return base_url, path

    def containsWhatsOnKeyword(self):
        keywords = ['/whats-on', '/whatson']
        return any(keyword in self.path.lower() for keyword in keywords)

    def containsExhibitionKeyword(self):
        keywords = ['/exhibition', '/exhibitions', '/art-exhibitions']
        return any(keyword in self.path.lower() for keyword in keywords)

    def containsEventKeyword(self):
        keywords = ['/event', '/events']
        return any(keyword in self.path.lower() for keyword in keywords)

    def containsPastKeyword(self):
        keywords = ['past', 'past-exhibitions', 'past-shows']
        return any(keyword in self.path.lower() for keyword in keywords)

    def containsYear(self):
        parts = self.path.split('/')
        last_part = parts[-1]
        return any(part.isdigit() and len(part) == 4 for part in last_part.split('-'))

    def containsYearInPath(self):
        pattern = r'/\d{4}/'
        return bool(re.search(pattern, self.path))

    def urlID(self, file_path=url_dict_path):
        base_url = self.base_url

        try:
            with open(file_path, 'r') as file:
                url_dict = json.load(file)
        except FileNotFoundError:
            url_dict = {}

        if base_url in url_dict:
            url_id = url_dict[base_url]
            return url_id
        else:
            new_url_id = len(url_dict) + 1
            url_dict[base_url] = new_url_id
            with open(file_path, 'w') as file:
                json.dump(url_dict, file)
            return new_url_id

    def run(self):
        data = {
            'containsWhatsOnKeyword': self.containsWhatsOnKeyword(),
            'containsExhibitionKeyword': self.containsExhibitionKeyword(),
            'containsEventKeyword': self.containsEventKeyword(),
            'containsPastKeyword': self.containsPastKeyword(),
            'containsYear': self.containsYear(),
            'containsYearInPath': self.containsYearInPath(),
            'baseUrlID': self.urlID(),
        }
        logging.debug(f"Features for URL {self.path}: {data}")
        return data
