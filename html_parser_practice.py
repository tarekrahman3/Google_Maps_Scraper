import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

text = []
url = []
rows = []

options = Options()

#options.headless = True
driver = webdriver.Chrome(options=options, executable_path='chromedriver')

Strings = [
 'The Right-Hand Task Force',
 'BRAC',
 'Grameenphone'
]
for string in Strings:
    time.sleep(3)
    driver.get('http://www.google.com')
    time.sleep(4)
    que = driver.find_element_by_xpath("//input[@name='q']")
    que.send_keys("site:LinkedIn.com/company/ ", string)
    time.sleep(4)
    que.send_keys(Keys.RETURN)
    time.sleep(4)
    col__1 = driver.find_element(By.ID, "rso").find_element_by_xpath('.//span[1]').text
    col_1 = ['Title:', col__1]
    text.append(col_1)
    col__2 = driver.find_element(By.ID, "rso").find_element_by_xpath('.//a').get_attribute('href')
    col_2 = ['Website:', col__2]
    url.append(col_2)
    row = [col_1, col_2]
    rows.append(row)

for data in rows:
    print(data)

driver.quit()
