from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import pygsheets
from price_parser import Price
import urllib3
import requests

# Variables to interact with the GSheets API, and the file we will be editing. Granting permission to access my google drive.
client = pygsheets.authorize(service_account_file = 'auction-prices-926dff328ce4.json')
spreadsht = client.open("auction items")

# Converts the worksheet into a pandas data frame.
worksht = spreadsht.worksheet_by_title("Sheet1").get_as_df()

# Browser to open the websites to be scraped. Added the option to not open the browser on screen.
op = webdriver.ChromeOptions()
op.add_argument('headless')
browser = webdriver.Chrome(options = op)

# A function that takes in a URL and finds the price, name and time left for an item.
def site_content(url):

    #Price, name and date variable to be scraped
    p = ''
    n = ''
    date=''

    # Checks if the value passed in is not null. Assuming that I put the right url into my spreadsheet.
    if url !='':

        #Checks if the page actually loads
        try:
            page = browser.get(url)
        except requests.ConnectionError:
            return''
        
        #Scrapes the price, name and formats the date into a formula to be put into the google sheet.
        p = Price.fromstring(browser.find_element(By.ID,'CurrentBidAmount_').text).amount_float
        n = browser.find_element(By.CLASS_NAME,'auction-Itemlist-Title').text
        date = "=TEXT(\"" + browser.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div[7]/div/div[3]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[2]').text[7:] + "\"-NOW(), \"DD:HH:MM\")"
    
    return p,n,date

# Applies the site_content to every website that is in the first column.
for i, row in worksht.iterrows():
    worksht.at[i,'PRICE'],worksht.at[i,'ITEM NAME'],worksht.at[i,'TIME LEFT'] = site_content(worksht.at[i,'LINK'])

# Updates the google sheet with the new values that were scraped for price, name and date.
spreadsht.worksheet_by_title("Sheet1").set_dataframe(worksht,"A1")