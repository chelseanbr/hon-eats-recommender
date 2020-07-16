# Honolulu Eats Recommender
<b>Recommender systems for restaurants in Honolulu, Hawai'i. Built with scraped Tripadvisor reviews.</b><br><i>by Chelsea Ramos</i>
 
## Table of Contents
1. [Introduction](#Introduction)
    * [Motivation](#Motivation)
    * [Web Scraping](#Web-Scraping)
        * [Pipeline](#Pipeline)
2. [EDA (Exploratory Data Analysis)](#Eda)
3. [Recommenders](#Recommenders)
    * [Popularity Recommender](#Popularity-Recommender)
    * [Content-Based Recommender](#Content-Based-Recommender)
    * [Collaborative Filtering Recommender](#Collaborative-Filtering-Recommender)
4. [Web App](#Web-App)
5. [Conclusion](#Conclusion)
6. [Next Steps](#Next-Steps)
7. [Reproducing This Project](#Reproducing-This-Project)
    * [File Tree](#File-Tree)
    * [Steps](#Steps)

## Introduction

### Motivation
<p>Aloha! 🌺  I am originally from Honolulu, so I grew up with the cuisines of Hawai'i. 🍽  Now, I am in the SF Bay Area for opportunities in tech & Data Science, but I still miss the local food back home! 💡  I decided to explore the variety of food choices in Honolulu and build a restaurant recommender so that you or I could easily find restaurants that suit our tastes or cravings for the next time we visit Honolulu. 🤙🏽  Mahalo for checking out this project! 🌴</p>

### Web Scraping

<h4><a href='https://www.tripadvisor.com/Restaurants-g60982-Honolulu_Oahu_Hawaii.html'>Tripadvisor Restaurants in Honolulu</a></h4>

![honolulu-page-top](/imgs/honolulu-page-top.png)
![honolulu-page-bot](/imgs/honolulu-page-bot.png)

I used <b>BeautifulSoup4</b> and <b>MongoDB (PyMongo)</b> to scrape and store data from <b>Tripadvisor</b> on <b><u>1,805</u> restaurants in Honolulu, Hawai'i</b> on <u>06/25/2020</u>. *This was done overnight with the help of an AWS EC2 instance.* Then, I parsed and converted the <b>unstructured text data (<u>15,903</u> documents)</b> from my MongoDB database into a structured json format (hon_eats_data.json --> [hon_eats_data.zip](/data/hon_eats_data.zip)) for use as a DataFrame with 20 columns (15,903 rows).

#### Flowchart
![web_scraping_flowchart](/imgs/web_scraping_flowchart.png)

1. [save_all_page_links.py](/src/save_all_page_links.py) scrapes all pages of <a href='https://www.tripadvisor.com/Restaurants-g60982-Honolulu_Oahu_Hawaii.html'>Tripadvisor Restaurants in Honolulu</a> to save all result links to [csv](/data/all_links.csv).
2. [scrape_reviews.py](/src/scrape_reviews.py) takes a csv with Tripadvisor restaurant links and scrapes/stores all review pages per link in MongoDB.
3. [save_dataframe.py](/src/save_dataframe.py) parses unstructured data in MongoDB to save to DataFrame/json.
* [saving_from_mongodb.ipynb](/saving_from_mongodb.ipynb) shows how I connected to MongoDB and parsed/saved data to a DataFrame.

## EDA

*In Progress*

[eda.ipynb](/eda.ipynb) shows my EDA so far.

## Recommenders

### Popularity Recommender


### Content-Based Recommender


### Collaborative Filtering Recommender


## Web App


## Conclusion


## Next Steps


## Reproducing This Project

### File Tree
```
.
├── README.md
├── data
│   ├── all_links.csv
│   └── hon_eats_data.zip
├── eda.ipynb
├── imgs
│   ├── honolulu-page-bot.png
│   ├── honolulu-page-top.png
│   └── web_scraping_flowchart.png
├── saving_from_mongodb.ipynb
└── src
    ├── save_all_page_links.py
    ├── save_dataframe.py
    └── scrape_reviews.py

3 directories, 10 files
```

### Steps
1. [Web Scraping](#Web-Scraping)


___

## [[Back to Top]](#Honolulu-Eats-Recommender)