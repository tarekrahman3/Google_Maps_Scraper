
# # Map Search Results LINK goes below
URL = 'https://www.google.com/maps/search/Restaurants/@23.1791086,89.502563,15z/data=!3m1!4b1'



from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import csv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--no-sandbox")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])
options.add_argument("--start-maximized")
options.add_argument('--ignore-certificate-errors')
#options.add_argument('user-data-dir="/home/tarek/Selenium_Projects/Project_LinkedIn/user_dir"')

col1=[]
col2=[]
col3=[]
col4=[]
col5=[]
col6=[]
col7=[]
col8=[]
col9=[]
col10=[]

def headers_loop():
	try:
		WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "section-result-content")))
	except:
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="section-result-content"]')))
		except:
			time.sleep(10)
	
	results= driver.find_elements_by_xpath("//div[contains(@class, 'scrollable-show section-layout-flex-vertical')]/div[@class='section-result']")
	#results=driver.find_elements_by_class_name('section-result-content')
	current_page=driver.find_element_by_xpath('//span[@class="n7lv7yjyC35__left"]').text
	print(f"current_page:{current_page}")
	i=0
	for i in range(len(results)): 
		results= driver.find_elements_by_xpath("//div[contains(@class, 'scrollable-show section-layout-flex-vertical')]/div[@class='section-result']")
		#results=driver.find_elements_by_class_name('section-result')
		title=results[i].find_element_by_xpath(".//h3[contains(@class, 'result-title')]").text
		try:
			rate=results[i].find_element_by_xpath(".//span[contains(@class, 'rating-score')]").text
		except:
			rate=''
		try:
			ratings=results[i].find_element_by_xpath(".//span[contains(@class, 'num-ratings')]").text
		except:
			ratings=''
		details=results[i].find_element_by_xpath(".//span[contains(@class, 'result-details')]").text
		location=results[i].find_element_by_xpath(".//span[contains(@class, 'result-location')]").text
		try:
			phones=results[i].find_element_by_xpath(".//span[contains(@class, 'phone-number')]").text
		except:
			phones=''
		try:
			website=results[i].find_element_by_xpath(".//div[contains(@class, 'result-action-container')]//a").get_attribute('href')
		except:
			website=''
		print(f">>'{title}'")
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
		
		wait_for_title=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "header-title")]')))
		business_url = driver.current_url
		try:
			address=driver.find_element_by_xpath('//button[contains(@data-item-id, "address")]').get_attribute('aria-label')
		except:
			address='N/A'
		try:
			address2=driver.find_element_by_xpath('//button[contains(@data-item-id, "data-item-id")]').text
		except:
			address2='N/A'
		print(f"...{address}")
		print(f"....... completed")
		col1.append(title)
		col2.append(rate)
		col3.append(ratings)
		col4.append(details)
		col5.append(location)
		col6.append(phones)
		col7.append(website)
		col8.append(address)
		col9.append(address2)
		col10.append(business_url)
		back_to_list=driver.find_element_by_xpath('//button[@class="section-back-to-list-button blue-link noprint"]')
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="section-back-to-list-button blue-link noprint"]')))
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
	try:
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='pane']/div/div[1]/div/div/div[4]/div[1]")))
	except:
		pass
	try:
		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "section-result-content")))
	except:
		time.sleep(20)
def data_frame():
	data = {'title': col1,
		'rate': col2,
		'ratings': col3,
		'details': col4,
		'location': col5,
		'phones': col6,
		'website': col7,
		'address': col8,
		'address2': col9,
		'business_url': col10
		}
	df = pd.DataFrame (data, columns = ['business_url', 'title','rate','ratings','details','location','phones','website','address','address2'])
	df.to_csv (r'google_map_export_data.csv', index = False, header=True)
	print(df)


driver=webdriver.Chrome(options=options, executable_path='/home/practice_environment/chromedriver')
driver.get(str(URL))

#functions
a=0
while True:
	try:
		headers_loop()
	except:
		pass
	try:
		next_pagination()
	except:
		break
a +=1
data_frame()
driver.quit()
	
print('############  Sequence Completed  ############')
