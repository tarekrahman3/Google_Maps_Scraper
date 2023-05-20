from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
from datetime import datetime


def scrap_info(driver):
    parent_box_xpath = "//body"
    business_url = f"{str(driver.current_url)}"

    try:
        title = driver.find_element(By.XPATH, parent_box_xpath + "//h1").text
    except:
        title = None
    try:
        address = (
            driver.find_element(
                By.XPATH,
                parent_box_xpath + '//button[contains(@aria-label,"Address:")]',
            )
            .get_attribute("aria-label")
            .replace("Address: ", "")
        )
    except:
        address = None
    try:
        driver.find_element(
            By.XPATH, parent_box_xpath + '//span[text()="Temporarily closed"]'
        )
        is_temporarily_closed = True
    except:
        is_temporarily_closed = False
    try:
        website = driver.find_element(
            By.XPATH, parent_box_xpath + '//a[@data-tooltip="Open website"]'
        ).get_attribute("href")
    except:
        website = None
    try:
        phones = (
            driver.find_element(
                By.XPATH,
                parent_box_xpath + "//button[contains(@aria-label, 'Phone:')]",
            )
            .get_attribute("aria-label")
            .replace("Phone:", "")
        )
    except:
        phones = None
    try:
        rate = (
            driver.find_element(
                By.XPATH,
                parent_box_xpath
                + '//div[div[@jsaction="pane.rating.moreReviews"]]//span[@aria-label]',
            )
            .get_attribute("aria-label")
            .replace("stars", "")
            .strip()
        )
    except:
        rate = None
    try:
        ratings = (
            driver.find_element(
                By.XPATH,
                parent_box_xpath + '//button[@jsaction="pane.rating.moreReviews"]',
            )
            .get_attribute("aria-label")
            .replace("reviews", "")
            .replace(" review", "")
            .strip()
        )
    except:
        ratings = None
    try:
        category = driver.find_element(
            By.XPATH,
            parent_box_xpath + '//button[@jsaction="pane.rating.category"]',
        ).text
    except:
        category = None
    try:
        open_days = driver.find_element(
            By.XPATH,
            parent_box_xpath + '//div[img[@aria-label="Hours"]]/following::div[1]',
        ).get_attribute("aria-label")
    except:
        open_days = None
    try:
        features = driver.find_element(
            By.XPATH,
            '//div[@role="region"]/button[contains(@jsaction,"pane.attributes")]',
        ).text
    except:
        features = None
    try:
        img_url = driver.find_element(
            By.XPATH,
            parent_box_xpath + '//button[starts-with(@aria-label,"Photo ")]/img',
        ).get_attribute("src")
    except:
        img_url = None
    try:
        driver.find_element(
            By.XPATH, parent_box_xpath + '//div[text()="Claim this business"]'
        )
        is_claimed = False
    except:
        is_claimed = True
    try:
        driver.find_element(
            By.XPATH,
            parent_box_xpath + '//span[text()="Identifies as Black-owned"]',
        )
        is_black_owned = True
    except:
        is_black_owned = False
    try:
        driver.find_element(
            By.XPATH,
            parent_box_xpath + "//span[text()='Closed']",
        )
        current_status = "Closed"
    except:
        current_status = "Open"
    try:
        plus_code = (
            driver.find_element(
                By.XPATH,
                parent_box_xpath + '//button[starts-with(@aria-label,"Plus code: ")]',
            )
            .get_attribute("aria-label")
            .replace("Plus code: ", "")
        )
    except:
        plus_code = None
    dict_array.append(
        {
            "input_url": url,
            "business_url": business_url,
            "title": title,
            "is_temporarily_closed": is_temporarily_closed,
            "rate": rate,
            "reviewCount": ratings,
            "category": category,
            "address": address,
            "attributes": features,
            "plus_code": plus_code,
            "website": website,
            "phones": phones,
            "open_days": open_days,
            "current_status": current_status,
            "img_url": img_url,
            "is_claimed": is_claimed,
            "is_black_owned": is_black_owned,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )
    print(i, dict_array[-1])


urls = pd.read_csv("map_business_scrap_input.csv").links.tolist()


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


dict_array = []
failed_list = []

for i, url in enumerate(urls):
    driver.get(url.replace("?hl=en", "") + "?hl=en")
    time.sleep(2)
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="article"]'))
        )
        failed_list.append({"failed_url": url})
    except TimeoutException:
        scrap_info(driver)
    pd.DataFrame(dict_array).to_csv(
        "backup_of_map_business_scrap_output.csv", index=False
    )
    pd.DataFrame(failed_list).to_csv(
        "backup_of_map_business_scrap_failed_list.csv", index=False
    )
driver.quit()
pd.DataFrame(dict_array).to_csv("map_business_scrap_output.csv", index=False)
pd.DataFrame(failed_list).to_csv("map_business_scrap_failed_list.csv", index=False)
