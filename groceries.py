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
driver.get("https://www.saveonfoods.com/sm/pickup/rsid/987/promotions")

soup = BeautifulSoup(driver.page_source, features="html.parser")

pages = 222 # soup.find('button', class_='') REVISE TO DYNAMICALLY GRAB MAX PAGE NUMBER
items = soup.find('div', class_='Listing-sc-1vfhaq2 iQljRa')
item_names = list()
item_prices = list()

nameAreaList = list()
priceAreaList = list()

for n in items:
    nameBig = n.find('span', class_='ProductCardTitle-sc-zzzom9 ivQxEH')  # finding the area with the product names
    name = nameBig.find('div', role='button')   # finding the actual names
    price = n.find('span', class_='ProductCardPrice-sc-urcjb')
    r = [i.string for i in name]
    s = [p.string for p in price]
    item_names.append(r)
    item_prices.append(s)

d = {'Names': item_names, 'Prices': item_prices}

print(d)

df = pd.DataFrame.from_dict(data=d)

print(df)

df.to_csv('products.csv', index=False, encoding='utf-8')

driver.close()
