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
worksht = spreadsht.worksheet_by_title("Sheet1").get_as_df()

print(worksht["PRICE"])
# Browser to open the websites to be scraped. Added the option to not open the browser on screen.
op = webdriver.ChromeOptions()
op.add_argument('headless')
browser = webdriver.Chrome(options = op)

def price_content(url):
    p = ''
    n = ''
    date=''
    if url !='':
        try:
            page = browser.get(url)
        except requests.ConnectionError:
            return''
        p = Price.fromstring(browser.find_element(By.ID,'CurrentBidAmount_').text).amount_float
        n = browser.find_element(By.CLASS_NAME,'auction-Itemlist-Title').text
        date = "=TEXT(\"" + browser.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div[7]/div/div[3]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[2]').text[7:] + "\"-NOW(), \"DD:HH:MM\")"
        print(date)
    return p,n,date


#prices.extend(zip(*worksht['LINK'].map(price_content)))

#worksht['PRICE'] = worksht['PRICE'].apply(price_content(*worksht['LINK']))

for i, row in worksht.iterrows():
    worksht.at[i,'PRICE'],worksht.at[i,'ITEM NAME'],worksht.at[i,'TIME LEFT'] = price_content(worksht.at[i,'LINK'])


print(worksht['PRICE'])
#worksht['PRICE'] = list(zip(*worksht['LINK'].map(price_content)))

spreadsht.worksheet_by_title("Sheet1").set_dataframe(worksht,"A1")
"""# Updates the column next to each website with the price of the current bid of the item.
for c in range(len(websites)):
    worksht.update_value((c+2,2),prices[c])

# Formats price to the left of each website and prints it console.                                                                    
res = "\n".join("{} \t {}".format(x, y) for x, y in zip(websites, prices))
print(res)
print(client.spreadsheet_titles())"""