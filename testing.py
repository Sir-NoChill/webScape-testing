import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

opts = Options()
opts.headless = True
driver = webdriver.Firefox(options=opts)

pages = 243  # TODO: soup.find('button', class_='') REVISE TO DYNAMICALLY GRAB MAX PAGE NUMBER
item_names = list()
item_prices = list()

nameAreaList = list()
priceAreaList = list()

pageNumber = 1
skip = 0

while pageNumber < (pages + 1):
    URL = 'https://www.saveonfoods.com/sm/pickup/rsid/987/promotions' + \
          '?page=' + str(pageNumber) + '&skip=' + str(skip)
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, features="html.parser")  # TODO: set to dynamically adapt to the website
    items = soup.find_all('div', class_='ColListing-sc-lcurnl')
    for n in items:
        nameBig = n.find('span', class_='ProductCardTitle-sc-ye20s3 iLdpjY')  # finding the area with the product names
        name = nameBig.find('div', role='button')  # finding the actual names
        price = n.find('span', class_='ProductCardPrice-sc-zgh1l1')
        r = [i.string for i in name]
        s = [p.string for p in price]
        item_names.append(r)
        item_prices.append(s)
    skip += 30
    pageNumber += 1

d = {'Names': item_names, 'Prices': item_prices}

df = pd.DataFrame.from_dict(data=d)
df.to_csv('products-saveon.csv', index=False, encoding='utf-8')   # TODO: dynamic file naming, iterable by date

# TODO is it possible to change the csv to xlsx directly?
#   can we export this data to a web application?

driver.close()
