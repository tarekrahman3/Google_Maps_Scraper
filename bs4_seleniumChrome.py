from selenium import webdriver
import os
import time
#from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd

options = Options()
#options.headless = True
driver = webdriver.Chrome(options=options, executable_path='chromedriver')

Search_Strings = ["red", "green", "blue", "purple"]
i = 0

while i < len(Search_Strings):

 driver.get("http://www.google.com")  
 time.sleep(3)
 que=driver.find_element_by_xpath("//input[@name='q']")
 que.send_keys(Search_Strings[i])
 time.sleep(3)
 que.send_keys(Keys.RETURN)
 time.sleep(3)
 
 """
 source = driver.page_source
 print (source)
 soup=BeautifulSoup(source, 'lxml')
 element=soup.find_all('h')
 print (soup)
 """
i += 1
