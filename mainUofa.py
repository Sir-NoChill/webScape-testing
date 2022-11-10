import string

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

URL = "https://apps.ualberta.ca/catalogue/search/results?keywords="

pages = 101  # 101  # soup.find('button', class_='') REVISE TO DYNAMICALLY GRAB MAX PAGE NUMBER
course_labels = list()
course_names = list()
course_credits = list()

nameAreaList = list()
priceAreaList = list()

pageNumber = 1

while pageNumber < (pages + 1):
    URL = 'https://apps.ualberta.ca/catalogue/search/results?keywords=&page=' + str(pageNumber)

    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    items = soup.find('div', class_='card')
    for n in items:
        if (n != "\n"):
            name = n.find('a')  # finding the area with the product names
            # name = nameBig.find('a')  # finding the actual names
            description = n.find('p')
            nmcredits = n.find('b')
            r = name
            if r is not None:
                r = r.text  # [str(i.string) for str(i) in name]
            s = description
            if s is not None:
                s = s.text  # [str(p.string) for str(p) in description]
            c = nmcredits
            if c is not None:
                c = c.text

            course_labels.append(r)
            course_names.append(s)
            course_credits.append(c)
    pageNumber += 1

d = {'Names': course_labels, 'Credits': course_credits, 'Descriptions': course_names}

df = pd.DataFrame.from_dict(data=d)
df.to_csv('classes-uofa.csv', index=False, encoding='utf-8')

driver.close()
