URL = input("Enter Google Map URL: ")
import re
keyword = re.search('\/maps\/search\/(.+)\/@', URL).group(1).replace('+',' ')
city = re.search('\!2s(.+?)\,', URL).group(1).replace('+', ' ')
Export_File_Name = f"{city} - {keyword}"

from selenium import webdriver
import time
from time import ctime
import csv
import os
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--no-sandbox")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])
#options.add_argument("--start-maximized")
options.add_argument('--ignore-certificate-errors')

col1 = []
col2 = []
col3 = []
col4 = []
col5 = []
col6 = []
col7 = []
col8 = []
col9 = []
col10 = []
col11 = []



def change_language():
	WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='searchbox-button']")))
	menu = driver.find_element_by_xpath("//button[@class='searchbox-button']").click()
	WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//button[contains(@class, "widget-languages")]')))
	lng_set = driver.find_element_by_xpath('//button[contains(@class, "widget-languages")]').click()
	WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="languages"]//ul[1]/li[11]/a')))
	en = driver.find_element_by_xpath('//*[@id="languages"]//ul[1]/li[11]/a').click()




def headers_loop():
	try:
		WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "section-result-content")))
	except:
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="section-result-content"]')))
		except:
			time.sleep(10)
	
	results= driver.find_elements_by_xpath("//div[contains(@class, 'scrollable-show')]/div[@class='section-result']")
	#results=driver.find_elements_by_class_name('section-result-content')
	current_page=driver.find_element_by_xpath('//span[@class="n7lv7yjyC35__left"]').text
	#print(f"current_page:{current_page}")
	i=0
	for i in range(len(results)):
		try:
			WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "section-result-content")))
		except:
			try:
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="section-result-content"]')))
			except:
				time.sleep(10)
		c_time = ctime()
		results = driver.find_elements_by_xpath("//div[contains(@class, 'scrollable-show')]/div[@class='section-result']")
		#results=driver.find_elements_by_class_name('section-result')
		
		try:
			rate = results[i].find_element_by_xpath(".//span[contains(@class, 'rating-score')]").text
		except:
			rate = ''
		try:
			ratings = results[i].find_element_by_xpath(".//span[contains(@class, 'num-ratings')]").text
		except:
			ratings = ''
		try:
			details = results[i].find_element_by_xpath(".//span[contains(@class, 'result-details')]").text
		except:
			details = ''
		try:
			location=results[i].find_element_by_xpath(".//span[contains(@class, 'result-location')]").text
		except:
			location = ''
		try:
			phones = results[i].find_element_by_xpath(".//span[contains(@class, 'phone-number')]").text
		except:
			phones = ''
		try:
			website = results[i].find_element_by_xpath(".//div[contains(@class, 'result-action-container')]//a").get_attribute('href')
		except:
			website = ''
		
		
		try:
			WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(@class, 'result-title')]")))
		except:
			time.sleep(5)
		try:
			WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "section-result-content")))
		except:
			time.sleep(5)
		try:
			results[i].click()
		except:
			try:
				time.sleep(10)
				results[i].click()
			except:
				results[i].click()
		wait_for_title = WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//h1[contains(@class, "section-hero-header-title")]')))
		business_url = f"{c_time} | {str(driver.current_url)}"
		title = driver.find_element_by_xpath(".//h1[contains(@class, 'section-hero-header')]").text
		try:
			address = driver.find_element_by_xpath('//button[contains(@data-item-id, "address")]').get_attribute('aria-label')
			
		except:
			address = ''
		print(f" >  {str((len(col1)+1))}   -    '{title}'")
		print(f"               {address}")
		col1.append(business_url)
		col2.append(title)
		col3.append(rate)
		col4.append(ratings)
		col5.append(details)
		col6.append(location)
		col7.append(phones)
		col8.append(website)
		col9.append(address)
		col10.append(city)
		col11.append(keyword)
		back_to_list=driver.find_element_by_xpath('//button[@class="section-back-to-list-button blue-link noprint"]')
		back_to_list.click()
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//h3[contains(@class, 'result-title')]")))
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(@class, 'result-title')]")))


def next_pagination():
	try:
		next_page=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="n7lv7yjyC35__section-pagination-button-next"]')))
		next_page.click()
	except:
		time.sleep(10)
		next_page.click()
	time.sleep(4)


def data_frame():
	csvtime = ctime()
	file_name=f"{csvtime} - {str(Export_File_Name)}.csv"
	data = {'keyword': col11,
	'city': col10,
	'business_url': col1,
	'title': col2,
	'rate': col3,
	'ratings': col4,
	'details': col5,
	'location': col6,
	'phones': col7,
	'website': col8,
	'address': col9
	}
	df = pd.DataFrame(data, columns = ['keyword','city' , 'business_url', 'title', 'rate', 'ratings', 'details', 'location', 'phones', 'website', 'address']).to_csv(file_name, index=None, header=True)
	print(f"new file created: {file_name}")


driver=webdriver.Chrome(options=options, executable_path='/home/tarek/MY_PROJECTS/Selenium_Projects/webdrivers/chromedriver')
driver.get(str(URL) + '?hl=en')
#disable_route_preview = driver.find_element_by_xpath('//*[@id="route-preview-controls-top-center"]//label/input')
#disable_route_preview.click()
#functions

#change_language()

while len(col1)<200:
	try:
		headers_loop()
	except:
		pass
	try:
		next_pagination()
		time.sleep(2)
	except:
		break

data_frame()
driver.quit()
	
print('############  Sequence Completed  ############')
