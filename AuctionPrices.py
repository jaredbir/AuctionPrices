from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd




browser = webdriver.Chrome()
browser.get("https://spear.prod2.maxanet.auction/Public/Auction/AuctionItemDetail?AuctionId=goMAUl%2fUnAsoaaS1nBIbSw%3d%3d&pageNumber=pf6Q%2bhJtdeleDd9FfYpy9w%3d%3d&pageSize=O5OaPaZE1XrTjGtTQItkaw%3d%3d&showFilter=iBcS%2b4ptjknZQtCojbueqQ%3d%3d&sortColumn=C9SY4KX74WJIILYqur0bmw%3d%3d&AuctionItemId=CIDcWOwD1o5FMiTUTBwHnA%3d%3d&Filter=ITUHdU2DoqWvw89vAOs0Dw%3d%3d")
content = browser.page_source
soup = BeautifulSoup(content)


    
name=soup.find('div', attrs={'class':'text-body'})
price = browser.find_element(By.ID, 'CurrentBidAmount_')

print(price.text)
