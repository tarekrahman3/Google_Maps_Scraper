from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from time import ctime
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")


driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

driver.execute_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
)
driver.maximize_window()
col1 = []
col2 = []
col3 = []


def search_region(each_region):
    driver.get("https://www.google.com/maps" + "?hl=en")
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="searchboxinput"]'))
    )
    search_box = driver.find_element_by_xpath('//*[@id="searchboxinput"]')
    search_box.click()
    search_box.send_keys(str(each_region))
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@class="suggestions"]/div/div[1]')
        )
    )
    evaluate_first_result = driver.find_element_by_xpath(
        '//*[@class="suggestions"]/div/div[1]'
    ).text
    search_box.send_keys(Keys.DOWN)
    search_box.send_keys(Keys.ENTER)
    location_url = driver.current_url
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button[contains(@aria-label, "Search nearby")]')
        )
    )
    search_nearby_button = driver.find_element_by_xpath(
        '//button[contains(@aria-label, "Search nearby")]'
    )
    search_nearby_button.click()


def search_by_keyword(each_keyword, each_region):
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="searchboxinput"]'))
    )
    business_search_box = driver.find_element_by_xpath('//*[@id="searchboxinput"]')
    business_search_box.click()
    business_search_box.clear()
    business_search_box.send_keys(each_keyword)
    business_search_box.send_keys(Keys.ENTER)
    time.sleep(5)
    generated_url = driver.current_url
    print(generated_url)
    col1.append(f"{str(each_region)}")
    col2.append(f"{str(each_keyword)}")
    col3.append(generated_url)


def gen_url():
    Regions = input(
        "Enter City & State Names (Example: Dallas, Texas; New York, NY) >> "
    )
    regions = Regions.split("; ")
    Keywords = input("Enter Keywords for nearby search (Example: Hospital; Clinic) >> ")
    keywords = Keywords.split("; ")
    for each_region in regions:
        try:
            search_region(each_region)
            for each_keyword in keywords:
                search_by_keyword(each_keyword, each_region)
        except Exception as e:
            print(e)
            pass
    driver.quit()
    data = {"city": col1, "keyword": col2, "generated_url": col3}
    file_name = "Generated Maps URL.csv"
    data_frame = pd.DataFrame(
        data, columns=["city", "keyword", "generated_url"]
    ).to_csv(file_name, index=None, header=True)


gen_url()
