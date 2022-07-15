import traceback
import time
import csv
import re
import pandas as pd
from datetime import datetime

from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

URL = input("input url:")
Export_File_Name = input("Export_File_Name:")


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


def headers_loop():
    parent_box_xpath = '//div[@tabindex="-1" and  @data-js-log-root and div[@data-js-log-root and @role="region"]]'

    results = driver.find_elements(
        By.XPATH, '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]'
    )
    i = 0
    while i < len(results):
        elements = driver.find_elements(
            By.XPATH,
            '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]//a',
        )
        driver.execute_script("arguments[0].scrollIntoView()", elements[i])
        time.sleep(1)
        elements = driver.find_elements(
            By.XPATH,
            '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]//a',
        )
        driver.execute_script("arguments[0].click()", elements[i])
        try:
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        parent_box_xpath + "/..//span[*[@viewBox]]",
                    )
                )
            )
        except TimeoutException:
            driver.execute_script(
                "arguments[0].click()",
                driver.find_elements(
                    By.XPATH,
                    '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]//a',
                )[i],
            )
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        parent_box_xpath + "/..//span[*[@viewBox]]",
                    )
                )
            )

        business_url = f"{str(driver.current_url)}"

        title = driver.find_element(By.XPATH, parent_box_xpath + "//h1").text
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
            website = driver.find_element(
                By.XPATH, parent_box_xpath + '//a[@data-tooltip="Open website"]'
            ).get_attribute("href")
        except:
            website = None
        try:
            phones = driver.find_element(
                By.XPATH, parent_box_xpath + "//button[contains(@aria-label, 'Phone:')]"
            ).get_attribute("aria-label")
        except:
            phones = None
        try:
            rate = driver.find_element(
                By.XPATH,
                parent_box_xpath
                + '//div[div[@jsaction="pane.rating.moreReviews"]]//span[@aria-label]',
            ).get_attribute("aria-label")
        except:
            rate = None
        try:
            ratings = driver.find_element(
                By.XPATH,
                parent_box_xpath + '//button[@jsaction="pane.rating.moreReviews"]',
            ).get_attribute("aria-label")
        except:
            ratings = None
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
        dict_array.append(
            {
                "business_url": business_url,
                "title": title,
                "rate": rate,
                "ratings": ratings,
                "open_days": open_days,
                "phones": phones,
                "website": website,
                "address": address,
                "features": features,
            }
        )
        print(i, dict_array[-1])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, parent_box_xpath + "/..//span[*[@viewBox]]")
            )
        )
        driver.execute_script(
            "arguments[0].click()",
            driver.find_element(By.XPATH, parent_box_xpath + "/..//span[*[@viewBox]]"),
        )
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element(
                (By.XPATH, parent_box_xpath + "/..//span[*[@viewBox]]")
            )
        )
        i += 1


def scroll_to_last_element(driver):
    driver.execute_script(
        "arguments[0].scrollIntoView()",
        driver.find_elements(
            By.XPATH,
            '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]',
        )[-1],
    )


def load_all_elements(driver):
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]',
            )
        )
    )
    results = len(
        driver.find_elements(
            By.XPATH,
            '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]',
        )
    )
    while True:
        scroll_to_last_element(driver)
        time.sleep(1)
        scroll_to_last_element(driver)
        current_results = len(
            driver.find_elements(
                By.XPATH,
                '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]',
            )
        )
        break_condition = False
        epoch_time = int(time.time())
        while True:
            scroll_to_last_element(driver)
            current_time = int(time.time())
            elapsed_time = datetime.fromtimestamp(
                current_time
            ) - datetime.fromtimestamp(epoch_time)
            try:
                end_result_notice = driver.find_element(
                    By.XPATH, """//*[text()="You've reached the end of the list."]"""
                )
            except:
                end_result_notice = None
            if current_results > results:
                print("new results found. Total Results: ", current_results)
                results = current_results
                epoch_time = int(time.time())
                break
            elif end_result_notice != None:
                break_condition = True
                break
            elif current_results == results and elapsed_time.seconds > 20:
                print("no new results. Total Results: ", current_results)
                break_condition = True
                break
        if break_condition == True:
            break


def write_csv():
    csvtime = time.ctime()
    file_name = f"{Export_File_Name}.csv"
    pd.DataFrame(dict_array).to_csv(file_name, index=False)
    print(f"new file created: {file_name}")


def main():
    driver.get(str(URL).replace("?hl=en", "") + "?hl=en")
    load_all_elements(driver)
    headers_loop()


try:
    main()
except Exception:
    print(traceback.format_exc())
finally:
    write_csv()
    driver.quit()

print("############  Sequence Completed  ############")