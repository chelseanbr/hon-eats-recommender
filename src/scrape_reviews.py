import warnings
warnings.filterwarnings('ignore')
from pymongo import MongoClient
import pandas as pd
# Requests sends and recieves HTTP requests.
import requests
# Beautiful Soup parses HTML documents in python.
from bs4 import BeautifulSoup

url_prefix = 'https://www.tripadvisor.com'

def get_next_review_page_link(url_prefix=url_prefix):
    """Return Next button's page link."""
    soup = BeautifulSoup(r.content, features="html.parser")
    div_next = soup.find("div", {"class": "unified ui_pagination"})
    link = div_next.find("a", {"class": "nav next ui_button primary cx_brand_refresh_phase2"})['href']
    return url_prefix + link

if __name__ == "__main__":
    print('Loading links csv and setting up database...')

    links_file_path = 'data/all_links.csv'
    links = pd.read_csv(links_file_path, index_col=0)
    print(links.shape)
    links = links['links'].tolist()
    print(type(links), len(links))

    client = MongoClient('localhost', 27017)
    db = client.tripadvisor_hon_eats_reviews
    pages = db.pages

    for link in links:
        print('Beginning to scrape reviews from {}...'.format(link))
        i = 1
        while True:
            r = requests.get(link)
            pages.insert_one({'html': r.content})
            print('pg{}'.format(i))
            try: 
                next_pg_link = get_next_review_page_link()
                i += 1
            except (AttributeError, TypeError):
                print('Reached last page ({}) for reviews.'.format(i))
                print(link)
                break
            link = next_pg_link