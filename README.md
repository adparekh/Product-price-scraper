# Product Price Tracker

The product price tracker is a python script that searches for a particular product from online shopping websites such as Amazon, and retrieves the product data from the website. This script scrapes essential product data from the Amazon website and stores it in JSON format. This JSON file is stored within the ```reports``` directory.

## About

This script has been written entirely in Python. Some libraries used are:

* Selenium: Web-scraping product information from the Amazon website.
* Json: Storing the product information

## Setup Instructions

1. This script uses the Selenium chrome webdriver to automate the web-scraping. Make sure to download the latest version of chromedrive. The official downloads can be found [here](https://chromedriver.chromium.org/downloads).

2. Setting up a virtual python environment. Execute the following code.
```buildoutcfg
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

3. Executing the python script.
```buildoutcfg
python3 product-price-tracker.py
```
