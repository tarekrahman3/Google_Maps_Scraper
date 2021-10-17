import undetected_chromedriver.v2 as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import re
import pandas as pd
URL = input("input url:")
try:
	URL = URL.replace('?hl=en', '')
except:
	pass
keyword = re.search('\/maps\/search\/(.+)\/@', URL).group(1).replace('+',' ')
try:
	city = re.search('\!2s(.+?)\,', URL).group(1).replace('+', ' ')
	Export_File_Name = f"{city} - {keyword}"
except:
	Export_File_Name = f"{keyword}"

driver = uc.Chrome()
dict_array = []
def headers_loop():
	try:
		WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@jsaction, 'mouseover:pane')]/a")))
	except:
		pass
	numbers = driver.find_elements_by_xpath('//div[@class="gm2-caption"]/div/span/span')
	length = (int(numbers[1].text)-int(numbers[0].text))+1
	for i in range(length):
		try:
			WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@jsaction, 'mouseover:pane')]/a")))
		except:
			pass
		current_results_ = driver.find_elements_by_xpath("//div[contains(@aria-label, 'Results')]/div//a[contains(@href, 'http')]")
		c_number = len(current_results_)
		we_need = i
		x = 0
		if i>=c_number:
			while True:
				try:
					r = driver.find_elements_by_xpath("//div[contains(@aria-label, 'Results')]/div//a[contains(@href, 'http')]")
					action = ActionChains(driver)
					action.move_to_element(r[(len(r))-1]).perform()
					r[(len(r))-1].location_once_scrolled_into_view
					if (len(r))>i:
						break
					else:
						pass
				except:
					pass
					x+=1
		else:
			pass
		results = driver.find_elements_by_xpath("//div[contains(@jsaction, 'mouseover:pane')]")
		c_time = time.ctime()

		rs = driver.find_elements_by_xpath("//div[contains(@jsaction, 'mouseover:pane')]/a")
		action = ActionChains(driver)
		rs[i-1].location_once_scrolled_into_view
		action.move_to_element(rs[i]).click().perform()	
		
		try:
			wait_for_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ".//h1[contains(@class, 'title')]")))
		except:
			'''rs = driver.find_elements_by_xpath("//div[contains(@aria-label, 'Results')]/div//a[contains(@href, 'http')]")
			action = ActionChains(driver)
			action.move_to_element(rs[i]).perform()	
			rs[i-1].location_once_scrolled_into_view
			rs[i].click()
			wait_for_title = WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//h1[contains(@class, "section-hero-header-title")]')))
			'''
			print('error')
		business_url = f"{str(driver.current_url)}"
		title = driver.find_element_by_xpath(".//h1[contains(@class, 'title')]").text
		try:
			address = driver.find_element_by_xpath('//button[contains(@data-item-id, "address")]').get_attribute('aria-label')
		except:
			address = ''
		try:
			website = driver.find_element_by_xpath("//button[contains(@aria-label, 'Website:')]").get_attribute('aria-label')
		except:
			website = ''
		try:
			phones = driver.find_element_by_xpath("//button[contains(@aria-label, 'Phone:')]").get_attribute('aria-label')
		except:
			phones = ''
		try:
			rate = driver.find_element_by_xpath('//ol[@class="section-star-array"]').get_attribute('aria-label')
		except:
			rate = ''
		try:
			ratings = driver.find_element_by_xpath("//span/button[contains(text(), 'review')]").text
		except:
			ratings = ''
		try:
			details = driver.find_element_by_xpath('//div[contains(@aria-label,"About")]').text
		except:
			details = ''

		print(f" >  {str((len(dict_array)+1))}   -    '{title}'")
		print(f"               {address}")
		dict_array.append({'time':c_time,
		'business_url': business_url,
		'title': title,
		'rate': rate,
		'ratings': ratings,
		'details': details,
		'phones': phones,
		'website': website,
		'address': address,
		'keyword': keyword
		})
		try:
			back_to_list=driver.find_element_by_xpath('//img[contains(@src,"arrow_back_black_24dp.png")]/..')
		except:
			pass
		back_to_list.click()
		time.sleep(1)
		try:
			WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@jsaction, 'mouseover:pane')]")))
		except:
			print('line 150 error')
			pass
	

def next_pagination():
		time.sleep(2)

		try:
			next_page=WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label=' Next page ']")))
			next_page.click()
			time.sleep(4)
			return int(1)
		except :
			print('paginaion failed')
			return int(0)

def write_csv():
	csvtime = time.ctime()
	file_name=f"{csvtime} - {str(Export_File_Name)}.csv"
	pd.DataFrame(dict_array).to_csv(file_name, index=False)
	print(f"new file created: {file_name}")

def main():
	driver.get(str(URL) + '?hl=en')
	while True:
		WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@aria-label,"Showing results")]')))
		try:
			headers_loop()
		except:
			break
		paginate = next_pagination()
		if paginate==0:
			break
		elif paginate==1:
			pass

try:
	main()

finally:
	write_csv()
	driver.quit()
print('############  Sequence Completed  ############')
