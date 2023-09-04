from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import pygsheets

# Variables to interact with the GSheets API, and the file we will be editing.
client = pygsheets.authorize(service_account_file = 'auction-prices-926dff328ce4.json')
spreadsht = client.open("auction items")
worksht = spreadsht.worksheet_by_title("Sheet1")

op = webdriver.ChromeOptions()
op.add_argument('headless')
browser = webdriver.Chrome(options = op)
browser.get("https://spear.prod2.maxanet.auction/Public/Auction/AuctionItemDetail?AuctionId=goMAUl%2fUnAsoaaS1nBIbSw%3d%3d&pageNumber=pf6Q%2bhJtdeleDd9FfYpy9w%3d%3d&pageSize=O5OaPaZE1XrTjGtTQItkaw%3d%3d&showFilter=iBcS%2b4ptjknZQtCojbueqQ%3d%3d&sortColumn=C9SY4KX74WJIILYqur0bmw%3d%3d&AuctionItemId=CIDcWOwD1o5FMiTUTBwHnA%3d%3d&Filter=ITUHdU2DoqWvw89vAOs0Dw%3d%3d")

prices = []
websites = worksht.get_col(1,returnas='matrix',include_tailing_empty = False)

for ws in websites:
    browser.get(ws)
    prices.append(browser.find_element(By.ID, 'CurrentBidAmount_').text)



print(*websites, sep = "\n")
print(*prices, sep = "\n")
print(client.spreadsheet_titles())