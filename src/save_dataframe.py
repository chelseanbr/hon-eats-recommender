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
    """Return list of info selected from current page"""
    # restaurant_name
    restaurant_name = soup.find("h1", {"class": "header heading masthead masthead_h1"}).getText()
    print(restaurant_name) #<-debug

    # description
    description = soup.find("meta", {"name": "description"})['content']
    
    # url
    url = soup.find("link", {"rel": "alternate", "hreflang": "en"})['href']
    
    
    # Listing Details
    
    # overall listing info
    listing_details = soup.find("div", {"id": "taplc_detail_overview_cards_0"})
    
    # top_details
    top_details = soup.find("div", {"id": "taplc_top_info_0"})
    top_details = top_details.findAll("a", {"class": "_2mn01bsa"})
    top_details =[top_detail.getText() for top_detail in top_details]
    top_details = ' | '.join(top_details)

    # main_details
    main_details = soup.find("div", {"id": "taplc_details_card_0"})

    # about
    try:
        about = main_details.find("div", {"class": "_1lSTB9ov"}).getText()
    except AttributeError:
        about = np.nan

    # check main tags for restaurant details
    tag_cats = main_details.findAll("div", {"class": "o3o2Iihq"})
    if len(tag_cats) == 0:
        # get details from another section
        details = soup.find("div", {"id": "taplc_detail_overview_cards_0"})
        # get detail categories
        detail_cats = details.findAll("div", {"class": "_14zKtJkz"})
        detail_cats = [detail_cat.getText() for detail_cat in detail_cats]
        details = details.findAll("div", {"class": "_1XLfiSsv"})
        details = [detail.getText() for detail in details]
    else:
        # proceed to get tags and their categories
        tag_cats = [tag_cat.getText() for tag_cat in tag_cats]
        details = main_details.findAll("div", {"class": "_2170bBgV"})
        details = [detail.getText() for detail in details]
        detail_cats = tag_cats

    details_dict = dict(zip(detail_cats, details))

    # populate detail fields
    try:
        price = details_dict['PRICE RANGE']
    except KeyError:
        price = np.nan
    try:
        diets = details_dict['Special Diets']
    except KeyError:
        diets = np.nan
    try:
        meals = details_dict['Meals']
    except KeyError:
        meals = np.nan
    try: 
        cuisines = details_dict['CUISINES']
    except KeyError:
        cuisines = np.nan
    try:
        features = details_dict['FEATURES']
    except KeyError:
        features = np.nan

    
    # overall_rating
    try: 
        overall_rating = listing_details.find("span", {"class": "r2Cf69qf"})
        overall_rating = float(overall_rating.getText()[:3])
    except AttributeError:
        overall_rating = np.nan

    # more overall ratings (food, service, value, atmosphere)
    more_overall_rating_types = listing_details.findAll("span", {"class": "_2vS3p6SS"})
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
        num_reviews = listing_details.find("a", {"class": "_10Iv7dOs"})
        num_reviews = int(num_reviews.getText().replace(',', '').split(' ')[0])
    except AttributeError:
        num_reviews = np.nan

    # ranking
    try:
        ranking = listing_details.findAll("div", {"class": "_3-W4EexF"})
        ranking = ranking[-1].getText()
    except IndexError:
        ranking = np.nan

    # location info
    location_info = listing_details.findAll("span", {"class": "_2saB_OSe"})

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
    
    
    # Reviews
    reviews_container = soup.find("div", {"class": "listContainer"})
    reviews = reviews_container.findAll("div", {"class": "prw_rup prw_reviews_review_resp"})
    review_data = []
    for review in reviews:
        curr_review = dict()
        try:
            curr_review['user_name'] = review.find("div", {"class": "info_text pointer_cursor"}).getText()
        except AttributeError:
            curr_review['user_name'] = np.nan
        bubble_rating_raw = review.find("span", {"class": "ui_bubble_rating"})
        try:
            curr_review['bubble_rating'] = int(str(bubble_rating_raw)[37:39])/10
        except ValueError:
            curr_review['bubble_rating'] = np.nan
        try:
            curr_review['review_contents'] = review.find("p", {"class": "partial_entry"}).getText().replace('...More', '')
        except AttributeError:
            curr_review['review_contents'] = np.nan
        review_data.append(curr_review)

    return [restaurant_name, description, url, top_details, about, price, diets, 
            meals, cuisines, features,
            overall_rating, food_rating, service_rating, value_rating, atmosphere_rating, 
            num_reviews, ranking, address, location, image_url, review_data]

if __name__ == "__main__":
    # Connect to MongoDB database
    print('Connecting to database...')
    client = MongoClient('localhost', 27017)
    db = client.tripadvisor_hon_eats_reviews
    pages = db.pages
    print('Getting data...')
    
    info = []
    # for page in pages.find({}).limit(10):
    cursor = pages.find({}, no_cursor_timeout=True)
    loop = 1
    for i in cursor:
        print(loop)
        soup = BeautifulSoup(i['html'], features="html.parser")
        curr_page_info = get_curr_page_info(soup)
        info.append(curr_page_info)
        loop += 1
    cursor.close()

    print('Saving...')
        
    info_df = pd.DataFrame(np.array(info),
                    columns=['restaurant_name', 'description', 'url', 'top_details', 'about', 
                            'price', 'diets', 
                            'meals', 'cuisines', 'features', 'overall_rating', 'food_rating', 
                            'service_rating', 
                            'value_rating', 'atmosphere_rating', 'num_reviews', 'ranking', 
                            'address', 'location', 'image_url', 'review_data'])

    # Save to JSON
    save_data_file_path = '../data/hon_eats_data.json'
    info_df.to_json(save_data_file_path)

    print('Saved data to ' + save_data_file_path)