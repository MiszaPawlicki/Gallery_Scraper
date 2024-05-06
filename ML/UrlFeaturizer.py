#reference: https://towardsdatascience.com/predicting-the-maliciousness-of-urls-24e12067be5

import json
import re

class UrlFeaturizer(object):
    def __init__(self, url):
        self.base_url, self.path = self.extractPath(url)


    def extractPath(self, url):
        # Remove protocol and www subdomain if present
        url = re.sub(r'^https?://(?:www\.)?', '', url)
        # Split the URL into base URL and path
        match = re.match(r'([^/]+)(.*)', url)
        base_url = match.group(1)
        path = match.group(2)
        return base_url, path

    def containsWhatsOnKeyword(self):
        keywords = ['/whats-on']
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
        # Split the path by slashes and consider the last part
        parts = self.path.split('/')
        last_part = parts[-1]
        # Check if the last part contains a four-digit number
        return any(part.isdigit() and len(part) == 4 for part in last_part.split('-'))

    def containsYearInPath(self):
        # Regular expression pattern to match four consecutive digits (year) surrounded by two slashes
        pattern = r'/\d{4}/'
        return bool(re.search(pattern, self.path))

    def urlID(self, file_path='url_dict.json'):
        base_url = self.base_url

        try:
            # Try to open the file containing the URL dictionary
            with open(file_path, 'r') as file:
                url_dict = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, create an empty dictionary
            url_dict = {}

        # Check if the base URL is present in the dictionary
        if base_url in url_dict:
            url_id = url_dict[base_url]
            return url_id
        else:
            # If the base URL is not present, generate a new ID
            new_url_id = len(url_dict) + 1
            # Add the base URL and its ID to the dictionary
            url_dict[base_url] = new_url_id
            # Write the updated dictionary back to the file
            with open(file_path, 'w') as file:
                json.dump(url_dict, file)
            return new_url_id

    def run(self):
        data = {}
        data['containsWhatsOnKeyword'] = self.containsWhatsOnKeyword()
        data['containsExhibitionKeyword'] = self.containsExhibitionKeyword()
        data['containsEventKeyword'] = self.containsEventKeyword()
        data['containsPastKeyword'] = self.containsPastKeyword()
        data['containsYear'] = self.containsYear()
        data['containsYearInPath'] = self.containsYearInPath()
        data['baseUrlID'] = self.urlID()
        return data

def main():
    featurizer = UrlFeaturizer('https://www.lissongallery.com/exhibitions/year/2009')

    print(featurizer.run())
    print(featurizer.base_url)
    print(featurizer.path)

if __name__ == "__main__":
    main()