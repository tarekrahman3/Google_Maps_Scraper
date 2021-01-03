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

rint ("          START driver.get           : %s" % time.ctime())
driver.get("http://www.google.com")
print ("          END driver.get             : %s" % time.ctime())

print ("          START time.sleep           : %s" % time.ctime())
time.sleep(2)
print ("          END time.sleep             : %s" % time.ctime())


print ("       Starting Process: Find Search Box")
que=driver.find_element_by_xpath("//input[@name='q']")

print ("          START typing in search box : %s" % time.ctime())

########################################################################
########################################################################
que.send_keys("Manchester FC Official Website")#### Search Query #######
########################################################################
########################################################################

que.send_keys(Keys.RETURN)
#send_keys article link - https://www.edureka.co/community/54152/google-search-automation-with-python-selenium
print ("          Search Result arrival time : %s" % time.ctime())
#not working #print ("       Current url : %s" % que.current_url())

time.sleep(5)

element=driver.find_element_by_xpath('//div[2]/div/div[1]/a')


href = element.get_attribute('href')
print (href)

#driver.quit()
