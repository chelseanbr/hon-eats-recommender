# Honolulu Eats Recommender
<i>Recommender systems for restaurants in Honolulu, Hawai'i built with scraped Tripadvisor reviews<br>by Chelsea Ramos</i>
 
## Table of Contents
1. [Introduction](#Introduction)
    * [Motivation](#Motivation)
    * [Web Scraping](#Web-Scraping)
2. [EDA](#Eda)
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
Aloha! I am originally from Honolulu, so I grew up with the cuisines of Hawai'i. Now, I am in the SF Bay Area for opportunities in tech & Data Science, but am missing the local foods back home! I decided to explore the variety of food choices in Honolulu and build a restaurant recommender so that you or I could easily find restaurants that suit our tastes or cravings the next time we visit Honolulu. Mahalo for checking out this project! :)

### Web Scraping
I used **BeautifulSoup4** and **MongoDB (PyMongo)** to scrape and store data from **Tripadvisor** on **<u>1,805</u> restaurants in Honolulu, HI** on <u>06/25/2020</u>. Then, I parsed and saved the unstructured data from MongoDB into a structured json format (/data/hon_eats_data.zip) for use as a DataFrame.

<h4><a href='https://www.tripadvisor.com/Restaurants-g60982-Honolulu_Oahu_Hawaii.html'>Tripadvisor Page for Restaurants in Honolulu</a></h4>

![honolulu-page-top](/imgs/honolulu-page-top.png)

![honolulu-page-bot](/imgs/honolulu-page-bot.png)


## EDA


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
│   └── hon_eats_data.zip
├── eda.ipynb
├── imgs
│   ├── honolulu-page-bot.png
│   └── honolulu-page-top.png
├── saving_from_mongodb.ipynb
└── src
    ├── save_all_page_links.py
    ├── save_dataframe.py
    └── scrape_reviews.py

3 directories, 9 files
```

### Steps
