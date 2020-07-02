import warnings
warnings.filterwarnings('ignore')
from pymongo import MongoClient
import pandas as pd
import numpy as np
# Requests sends and recieves HTTP requests.
import requests
# Beautiful Soup parses HTML documents in python.
from bs4 import BeautifulSoup

def get_curr_page_info(soup):
    # restaurant_name
    restaurant_name = soup.find("h1", {"class": "header heading masthead masthead_h1"}).getText()
#     print(restaurant_name) #<-debug

    # description
    description = soup.find("meta", {"name": "description"})['content']
    
    # url
    url = soup.find("link", {"rel": "alternate", "hreflang": "en"})['href']
    
    # overall listing info
    listing_details = soup.find("div", {"id": "taplc_detail_overview_cards_0"})
    
    # top_details
    top_details = soup.find("div", {"id": "taplc_top_info_0"})
    top_details = top_details.findAll("a", {"class": "restaurants-detail-top-info-TopInfo__tagLink--2LkIo"})
    top_details =[top_detail.getText() for top_detail in top_details]
    top_details = ' | '.join(top_details)

    # main_details
    main_details = soup.find("div", {"id": "taplc_details_card_0"})

    # about
    try:
        about = main_details.find("div", {"class": "restaurants-details-card-DesktopView__desktopAboutText--1VvQH"}).getText()
    except AttributeError:
        about = np.nan
    
    # tags
    tags = main_details.findAll("div", {"class": "restaurants-details-card-TagCategories__tagText--Yt3iG"})
    tags = [tag.getText() for tag in tags]
    tags = ' | '.join(tags)
    
    # more_details
    more_details = soup.find("div", {"id": "taplc_detail_overview_cards_0"})
    more_details = more_details.findAll("div", {"class": "restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h"})
    more_details = [more_detail.getText() for more_detail in more_details]
    more_details = ' | '.join(more_details)

    # overall_rating
    try: 
        overall_rating = listing_details.find("span", {"class": "restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--nohTl"})
        overall_rating = float(overall_rating.getText()[:3])
    except AttributeError:
        overall_rating = np.nan
        
    # more overall ratings (food, service, value, atmosphere)
    more_overall_rating_types = listing_details.findAll("span", {"class": "restaurants-detail-overview-cards-RatingsOverviewCard__ratingText--1P1Lq"})
    more_overall_rating_types = [rating.getText() for rating in more_overall_rating_types]

    more_overall_ratings_raw = listing_details.findAll("span", {"class": "ui_bubble_rating"})[1:]
    more_overall_ratings = [int(str(rating)[37:39])/10 for rating in more_overall_ratings_raw]

    more_overall_ratings_dict = {}
    for i in range(len(more_overall_rating_types)):
        more_overall_ratings_dict[more_overall_rating_types[i]] = more_overall_ratings[i]

    try: 
        food_rating = more_overall_ratings_dict['Food']
    except KeyError:
        food_rating = np.nan
    try: 
        service_rating = more_overall_ratings_dict['Service']
    except KeyError:
        service_rating = np.nan
    try: 
        value_rating = more_overall_ratings_dict['Value']
    except KeyError:
        value_rating = np.nan
    try: 
        atmosphere_rating = more_overall_ratings_dict['Atmosphere']
    except KeyError:
        atmosphere_rating = np.nan
        
    # num_reviews
    try: 
        num_reviews = listing_details.find("a", {"class": "restaurants-detail-overview-cards-RatingsOverviewCard__ratingCount--DFxkG"})
        num_reviews = int(num_reviews.getText().replace(',', '').split(' ')[0])
    except AttributeError:
        num_reviews = np.nan
    
    # ranking
    try:
        ranking = listing_details.findAll("div", {"class": "restaurants-detail-overview-cards-RatingsOverviewCard__ranking--17CmN"})
        ranking = ranking[-1].getText()
    except IndexError:
        ranking = np.nan
        
    # location info
    location_info = listing_details.findAll("span", {"class": "restaurants-detail-overview-cards-LocationOverviewCard__detailLinkText--co3ei"})

    # address
    try:
        address = location_info[0].getText()
    except IndexError:
        address = np.nan

    # location
    try: 
        location = location_info[1]
        location = location.findAll("div")[-1].getText()
    except IndexError:
        location = np.nan
        
    # image_url
    try: 
        image_urls = soup.find("div", {"class": "mosaic_photos"})
        image_url = image_urls.find("img", {"class": "basicImg"})['data-lazyurl']
    except TypeError:
        image_url = ''

    # user_names
    user_names = []
    user_names_raw = soup.findAll("div", {"class": "info_text pointer_cursor"})
    for name in user_names_raw:
        user_names.append(name.getText())

    # bubble_ratings
    bubble_ratings = []
    reviews = soup.find("div", {"class": "listContainer"})
    bubble_ratings_raw = reviews.findAll("span", {"class": "ui_bubble_rating"})
    for rating in bubble_ratings_raw:
        bubble_ratings.append(int(str(rating)[37:39])/10)

    # review_contents
    review_contents = []
    review_contents_raw = reviews.findAll("p", {"class": "partial_entry"})
    for review in review_contents_raw:
        review_contents.append(review.getText().replace('...More', ''))

    return [restaurant_name, description, url, top_details, about, tags, more_details, 
            overall_rating, food_rating, service_rating, value_rating, atmosphere_rating, 
            num_reviews, ranking, address, location, image_url, user_names, bubble_ratings, review_contents]

if __name__ == "__main__":
    print('Connecting to database...')
    client = MongoClient('localhost', 27017)
    db = client.tripadvisor_hon_eats_reviews
    pages = db.pages
    print('Getting data...')
    
    info = []
    # for page in pages.find({}).limit(10):
    for page in pages.find({}):
        soup = BeautifulSoup(page['html'], features="html.parser")
        curr_page_info = get_curr_page_info(soup)
        info.append(curr_page_info)
        
    info_df = pd.DataFrame(np.array(info),
                    columns=['restaurant_name', 'url', 'description', 'image_url', 'user_names', 
                                'bubble_ratings', 'review_contents'])

    save_data_file_path = '../data/hon_eats_data.csv'
    info_df.to_csv(save_data_file_path)

    print('Saved data to ' + save_data_file_path)