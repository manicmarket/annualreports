from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import json
import time
import pandas as pd
from lxml import html
import numpy as np
import re
import os
import xml.etree.ElementTree as ET

reader = pd.read_excel("cid.xlsx", engine='openpyxl').values.tolist()
cik = []
for i in reader:
    if str(i[3]) == 'nan':
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        driver = webdriver.Chrome('/home/tst/Downloads/chromedriver_linux64/chromedriver', desired_capabilities=capa)
        driver.set_page_load_timeout(1)
        driver.get(f'https://data.sec.gov/rss?cik={i[1]}&type=10-K')
        time.sleep(5)
        d = driver.find_element(By.TAG_NAME, 'pre').text
        result = re.search('<filing-href>(.*)</filing-href>', d)
        if result:
            i[3] = result.group(1)
        driver.close()
        print(i)
    cik.append(i)

writer = pd.ExcelWriter("cid.xlsx")
df = pd.DataFrame(cik)
df.to_excel(writer)
writer.save()


