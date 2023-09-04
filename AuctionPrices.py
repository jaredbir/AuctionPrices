from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import pygsheets
from price_parser import Price
import numpy as np

# Variables to interact with the GSheets API, and the file we will be editing. Granting permission to access my google drive.
client = pygsheets.authorize(service_account_file = 'auction-prices-926dff328ce4.json')
spreadsht = client.open("auction items")
worksht = spreadsht.worksheet_by_title("Sheet1")

# Browser to open the websites to be scraped. Added the option to not open the browser on screen.
op = webdriver.ChromeOptions()
op.add_argument('headless')
browser = webdriver.Chrome(options = op)

# List to update prices scraped from websites. Gathers all websites from the first column of the Google Sheet spreadsheet.
prices = []
websites = worksht.get_col(1,returnas ='matrix',include_tailing_empty = False)

# Scrapes prices and formats them to only the float value from their respective websites.
for ws in websites:
    browser.get(ws)
    prices.append(Price.fromstring(browser.find_element(By.ID, 'CurrentBidAmount_').text).amount_float)

# Updates the column next to each website with the price of the current bid of the item.
for c in range(len(websites)):
    worksht.update_value((c+1,2),prices[c])

res = "\n".join("{} \t {}".format(x, y) for x, y in zip(websites, prices))
print(res)
print(client.spreadsheet_titles())