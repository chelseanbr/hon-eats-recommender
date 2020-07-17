import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def load_data(data_file='data/hon_eats_data.json'):
    """Takes json file name, loads and returns DataFrame"""
    df = pd.read_json(data_file)
    return df

def get_nonzero_reviews_df(df):
    """Takes df, returns df including only restaurants with at least 1 review"""
    df_nonzero_reviews = df[(df['review_data'].apply(lambda x: len(x))>=1) \
        & (~df['num_reviews'].isnull())].copy()
    return df_nonzero_reviews

def unnest_review_data(df):
    """Takes df, returns df with review data unnested"""
    # Get subset of columns
    df_reviews = df[['url', 'review_data']]
    # Unnest
    df_reviews_unnested = pd.concat(df_reviews['review_data'].apply(pd.DataFrame).tolist(),
            keys=df_reviews["url"]).reset_index(level="url")
    # Drop duplicate rows
    df_reviews_unnested.drop_duplicates(inplace=True)
    # Include more columns for merging later
    df_reviews_full = pd.merge(df_nonzero_reviews[['restaurant_name', 'description', 
                                                'address', 'url']], df_reviews_unnested, on='url')
    return df_reviews_full

def clean_restaurant_data(df):
    """Takes df, returns df with restaurant data cleaned up"""
    df_restaurants = df.drop(columns=['url', 'review_data'])
    # Drop duplicate rows
    df_restaurants.drop_duplicates(inplace=True)
    # Drop Null Rankings
    df_restaurants[df_restaurants['ranking'].isna()==True]
    # Drop restaurants with null rankings, confirmed CLOSED on Tripadvisor
    df_restaurants.drop(index=df_restaurants[df_restaurants['ranking'].isna()==True].index, \
        inplace=True)
    # Fill Null Locations
    df_restaurants['location'].fillna("N/A", inplace=True)
    return df_restaurants

def geocode_addresses(df, output_file='data/geocoded_addresses.csv'):
    """Takes df with addresses, saves df with 'latitude', 'longitude', 'altitude' added to csv"""
    df_address = df[['restaurant_name', 'description', 'address']]
    locator = Nominatim(user_agent="myGeocoder")
    # 1 - convenient function to delay between geocoding calls
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    print('Geocoding addresses...')
    # 2- - create location column
    df_address['location'] = df_address['address'].apply(geocode)
    # 3 - create longitude, laatitude and altitude from location column (returns tuple)
    df_address['point'] = df_address['location'].apply(lambda loc: tuple(loc.point) if loc else None)
    # 4 - split point column into latitude, longitude and altitude columns
    df_address[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df_address['point'].tolist(), index=df_address.index)
    df_address.to_csv(output_file)
    print('Saved to ' + output_file)

if __name__ == "__main__":
    df = load_data()
    df = get_nonzero_reviews_df(df)
    df = clean_restaurant_data(df)
    geocode_addresses(df)