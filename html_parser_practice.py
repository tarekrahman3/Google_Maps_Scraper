from selenium import webdriver
import os
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import lxml


options = Options()
#options.headless = True
driver = webdriver.Chrome(options=options, executable_path='chromedriver')
driver.get("http://www.google.com")  
time.sleep(3)

que=driver.find_element_by_xpath("//input[@name='q']")
que.send_keys('site:reddit.com bs4 tutorial')
time.sleep(3)
que.send_keys(Keys.RETURN)
time.sleep(4)

html=driver.page_source
soup=BeautifulSoup(html, "lxml")

for a in soup.find_all('a', href=True):
    print ("URL:", a['href'])
