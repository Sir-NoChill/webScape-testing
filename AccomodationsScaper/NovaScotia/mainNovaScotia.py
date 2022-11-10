import string

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

### SETUP ###

opts = Options()
opts.headless = True
driver = webdriver.Firefox(options=opts)

URL_gen = "https://www.novascotia.com/places-to-stay/accommodations/clairestone-inn/"

pages = 8303   # soup.find('button', class_='') REVISE TO DYNAMICALLY GRAB MAX PAGE NUMBER
category = list()
price_low = list()
price_hig = list()
description = list()
names = list()
URLS = list()

pageNumber = 1

### END SETUP ###

### FUNCTIONS ###


### END FUNCTIONS ###

while pageNumber <= pages:
    # Setup
    URL = str(URL_gen + str(pageNumber))
    print('getting URL: ' + URL)
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    # End Setup

    print('Grabbing info')

    category_sing = soup.find('p', class_='type')  # find the type of the attraction on the page

    if (category_sing is not None) and (category_sing.text == 'Accommodations'):
        price_sing = soup.find('div', class_="MuiGrid-root item MuiGrid-item MuiGrid-grid-xs-12").next_sibling.text
        # Price (Format: 'PRICE$##(#).## to $##(#).##')
        description_sing = soup.find('div', class_="description").text  # the description
        names_sing = category_sing.next_sibling.text  # the name of the accomodation
    else:
        pageNumber += 1
        continue

    # Reformat of the price_low tag
    try:
        price_reformat_low = price_sing.split('$')[1].split(' ')[0]
        price_reformat_hig = price_sing.split('$')[2]
    except IndexError:
        price_reformat_low = None
        price_reformat_hig = None
        print("error in acquiring pricing information")

    category.append(category_sing.text)
    price_low.append(price_reformat_low)
    price_hig.append(price_reformat_hig)
    description.append(description_sing.strip())
    names.append(names_sing.strip())
    URLS.append(URL)
    print(names_sing + " " + str(price_reformat_low))
    pageNumber += 1

d = {'Names': names, 'Categories': category, 'Description': description, 'Lowest Price': price_low, 'Highest Price': price_hig, 'URL': URLS}

df = pd.DataFrame.from_dict(data=d)
df.to_csv('nova_scotia_accomodations.csv', index=False, encoding='utf-8')

driver.close()
