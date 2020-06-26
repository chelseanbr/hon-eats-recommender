import pandas as pd
# Requests sends and recieves HTTP requests.
import requests
# Beautiful Soup parses HTML documents in python.
from bs4 import BeautifulSoup

url_prefix = 'https://www.tripadvisor.com'

def get_all_page_links(url_prefix=url_prefix):
    """Return all page links for restaurants in Honolulu."""
    links = []
    div_links = soup.find_all("a", {"class": "_2uEVo25r _3tdrXOp7"})
    links = []
    for item in div_links:
        links.append(url_prefix + item['href'])
    return links

def get_next_page_link(url_prefix=url_prefix):
    """Return Next button's page link."""
    div_next = soup.find("div", {"class": "unified pagination js_pageLinks"})
    link = div_next.find("a", {"class": "nav next rndBtn ui_button primary taLnk"})['href']
    return url_prefix + link

if __name__ == "__main__":
    print('Getting links...')
    hon_top_page = 'https://www.tripadvisor.com/Restaurants-g60982-Honolulu_Oahu_Hawaii.html'

    r = requests.get(hon_top_page)
    # r.status_code # Check for status code 200
    soup = BeautifulSoup(r.content, features="html.parser")

    all_links = []
    all_links.extend(get_all_page_links())
    next_page = get_next_page_link()

    while True:
        r = requests.get(next_page)
        soup = BeautifulSoup(r.content, features="html.parser")
        all_links.extend(get_all_page_links())
        # Try to go to next page until "Next" button is unavailable
        try:
            next_page = get_next_page_link()
        except:
            break
    
    links_set = set(all_links)
    links_df = pd.DataFrame(links_set, columns=['links'])
    links_file_path = '../data/all_links.csv'
    links_df.to_csv(links_file_path)

    print('Saved links to ' + links_file_path)