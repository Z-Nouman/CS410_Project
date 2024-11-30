# Wikipedia Crawler
CS 410 Text Information Systems Course Project

Author: Zaid Al Nouman

## About
This repository contains a Python script that acts as a Wikipedia Crawler. This crawler, provided a starting article and target article, aims to find the shortest "path" between the two articles via direct links on each article. This crawler can also be used to scrape the HTML from all scraped pages, allowing one to input an invalid target link to scrape all of Wikipedia in theory. 

## Installation
Using a base conda environment with no additional installations is all that is required to run this script. To install Anaconda on your machine, follow these instructions: https://docs.anaconda.com/anaconda/install/. Next, create a fresh environemnt with something like:

``conda create --name <environment name>``

Then you should be all good to go!

## Controls
The user has a few variables to control to modify the result of the script:

``start_link``: Starting article for the crawler, of the format /wiki/<article_name> (ex. "/wiki/Information_retrieval")

``target_link``: Target link for the crawler to find a shortest path to, of the format /wiki/<article_name> (ex. "/wiki/Central_processing_unit")

``max_depth``: Maximum depth for the BFS before stopping the search. To remove any limits, set to ``math.inf``

``max_articles``: Maximum number of articles to scrape before stopping the search. To remove any limits, set to ``math.inf``

``save_articles``: Boolean to control whether the crawler saves the raw HTML of all scraped articles. Set to True to collect articles for possible future applications, such as a text corpus.
