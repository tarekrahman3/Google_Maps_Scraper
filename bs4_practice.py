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
que.send_keys('Beautifulsoup Parse Tutorial')
time.sleep(3)
que.send_keys(Keys.RETURN)
time.sleep(4)
a=driver.page_source
name = 'a1.txt'
try:
    file = open(name,'w',encoding='utf-8')
    file.write(a)
    file.close()

except:
     print('page'+str(x)+'\n')
       
a=""
time.sleep(3)
   
#driver.close()
