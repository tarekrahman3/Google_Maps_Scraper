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


def start_browser():
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
    return driver


def search_region(driver, each_region):
    driver.get("https://www.google.com/maps" + "?hl=en")
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="searchboxinput"]'))
    )
    search_box = driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
    search_box.click()
    search_box.send_keys(str(each_region))
    search_box.send_keys(Keys.ENTER)
    location_url = driver.current_url
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button[contains(@aria-label, "Search nearby")]')
        )
    )
    search_nearby_button = driver.find_element(
        By.XPATH, '//button[contains(@aria-label, "Search nearby")]'
    )
    search_nearby_button.click()


def search_by_keyword(driver, each_keyword, each_region, output_list):
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="searchboxinput"]'))
    )
    business_search_box = driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
    business_search_box.click()
    business_search_box.clear()
    business_search_box.send_keys(each_keyword)
    business_search_box.send_keys(Keys.ENTER)
    time.sleep(5)
    generated_url = driver.current_url
    output_list.append(
        {
            "Region": str(each_region),
            "Searched Keyword": each_keyword,
            "Generated URL": generated_url,
        }
    )
    print(len(output_list), output_list[-1])


def main():
    Regions = input(
        "Enter City & State Names (Example: Dallas, Texas; New York, NY) >> "
    )
    regions = Regions.split("; ")
    Keywords = input("Enter Keywords for nearby search (Example: Hospital; Clinic) >> ")
    keywords = Keywords.split("; ")

    driver = start_browser()

    output_list = []

    for each_region in regions:
        try:
            search_region(driver, each_region)
            for each_keyword in keywords:
                search_by_keyword(driver, each_keyword, each_region, output_list)
        except Exception as e:
            print(e)
            pass
        pd.DataFrame(output_list).to_csv(
            "Generated_Maps_URLs (Backup).csv", index=None, header=True
        )

    driver.quit()

    pd.DataFrame(output_list).to_csv("Generated_Maps_URLs.csv", index=None, header=True)


if __name__ == "__main__":
    main()
