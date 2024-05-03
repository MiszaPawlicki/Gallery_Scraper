#reference: https://towardsdatascience.com/predicting-the-maliciousness-of-urls-24e12067be5
import re
from urllib.parse import urlparse

class UrlFeaturizer(object):
    def __init__(self, url):
        self.url = self.extractPath(url)
        # other initialization code...

    def extractPath(self, url):
        # Remove protocol and www subdomain if present
        url = re.sub(r'^https?://(?:www\.)?', '', url)
        # Remove domain and extract path
        path = re.sub(r'^[^/]+', '', url)
        return path
    def containsWhatsOnKeyword(self):
        keywords = ['whats-on']
        return any(keyword in self.url.lower() for keyword in keywords)

    def containsExhibitionKeyword(self):
        keywords = ['exhibition', 'exhibitions']
        return any(keyword in self.url.lower() for keyword in keywords)

    def containsEventKeyword(self):
        keywords = ['event', 'events']
        return any(keyword in self.url.lower() for keyword in keywords)

    def containsPastKeyword(self):
        keywords = ['past', 'past-exhibitions', 'past-shows']
        return any(keyword in self.url.lower() for keyword in keywords)
        return -1
    def containsYear(self):
        # Regular expression pattern to match four consecutive digits (year)
        pattern = r'\b\d{4}\b'
        return bool(re.search(pattern, self.url))

    def pathLength(self):
        # Count the number of '/' characters in the URL path
        path = urlparse(self.url).path
        return path.count('/')

    def run(self):
        data = {}
        # existing feature extraction...

        ## Additional feature extraction

        data['containsWhatsOnKeyword'] = self.containsWhatsOnKeyword()
        data['containsExhibitionKeyword'] = self.containsExhibitionKeyword()
        data['containsEventKeyword'] = self.containsEventKeyword()
        data['containsPastKeyword'] = self.containsPastKeyword()
        data['containsYear'] = self.containsYear()
        data['pathLength'] = self.pathLength()
        return data
