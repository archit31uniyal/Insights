import requests
import re
from bs4 import BeautifulSoup

import pickle as pkl

class Review:
    def __init__(self, base_url, num_pages= 5, rating= [], date= [], text = []):
        self.base_url = base_url
        self.rating = rating
        self.date = date
        self.text = text
        self.num_pages = num_pages
    
    def fetch_reviews(self):
        url2 = self.base_url
        start = 0
        end = 10* self.num_pages

        while start < end:
            url = url2 + "?start=" + str(start)
            start +=10
            page = requests.get(url)
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, 'html.parser')
                try:
                    reviews = soup.find(string='Recommended Reviews').find_parent('section')
                    reviews = reviews.select('div[aria-label$="star rating"]')
                    for review in reviews:
                        self.rating.append(float(re.findall('[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', review['aria-label'])[0]))
                        self.date.append(review.find_next('span').text)
                        self.text.append(review.find_next('span', lang=True).text)
                except:
                    print('No parent section')
                    pass
            else:
                print('Page not found')
                continue

def save_pickle(obj, filename):
    with open(filename, 'wb') as f:
        pkl.dump(obj, f)

def load_pickle(filename):
    with open(filename, 'rb') as f:
        return pkl.load(f)