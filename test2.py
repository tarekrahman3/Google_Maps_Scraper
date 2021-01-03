from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firebox.options import Options
from selenium.webdriver.common.keys import Keys


options = Options()
#(Turn on Background mode)options.headless = True
#options.log.level = "trace"
driver = webdriver.Firefox(options=options,
          executable_path='path')
#################################################


### {SAMI}    Eikhan theke main process suru     #####
### {SAMI}    Chrome webdriver use kore Selenium module google er home page open korbe     #####

driver.get("http://www.google.com")  
time.sleep(6)

### {SAMI}    Google er Search box find korar xpath     #####
que=driver.find_element_by_xpath("//input[@name='q']")

### {SAMI}    search box e search query likhbe     #####
que.send_keys("site:linkedin.com/company Microsofft")
time.sleep(6)

que.send_keys(Keys.RETURN)
time.sleep(5)

element=driver.find_element_by_xpath('//div[2]/div/div[1]/a')
href = element.get_attribute('href')

print (href)

#driver.quit()
