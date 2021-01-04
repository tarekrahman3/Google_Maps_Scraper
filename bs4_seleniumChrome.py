from selenium import webdriver
import os
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


options = Options()
#options.headless = True
driver = webdriver.Chrome(options=options, executable_path='chromedriver')

Search_Strings = ["LinkedIn", "Crunchbase", "Twitter", "Apple"]
i = 0
for i in range(len(Search_Strings)):
 driver.get("http://www.google.com")  
 time.sleep(3)
 que=driver.find_element_by_xpath("//input[@name='q']")
 que.send_keys(Search_Strings[i])
 time.sleep(3)
 que.send_keys(Keys.RETURN)
 time.sleep(3)
i += 1
