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


def start_browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    time.sleep(1)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    driver.maximize_window()
    return driver


def headers_loop(driver, url, dict_array):
    parent_box_xpath = '//div[@tabindex="-1" and  @data-js-log-root and div[@data-js-log-root and @role="region"]]'

    results = driver.find_elements(
        By.XPATH,
        '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]//div[@role="article"]/a',
    )
    i = 0
    while i < len(results):
        elements = driver.find_elements(
            By.XPATH,
            '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]//div[@role="article"]/a',
        )
        driver.execute_script("arguments[0].scrollIntoView()", elements[i])
        time.sleep(1)
        elements = driver.find_elements(
            By.XPATH,
            '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]//div[@role="article"]/a',
        )
        elements[i].location_once_scrolled_into_view
        try:
            driver.execute_script("arguments[0].click()", elements[i])
        except:
            input("stuck")
        try:
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        parent_box_xpath
                        + "/..//div[3]/span/button//*[local-name()='svg']/..",
                    )
                )
            )
        except TimeoutException:
            driver.execute_script(
                "arguments[0].click()",
                driver.find_elements(
                    By.XPATH,
                    '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]//div[@role="article"]/a',
                )[i],
            )
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        parent_box_xpath
                        + "/..//div[3]/span/button//*[local-name()='svg']/..",
                    )
                )
            )

        business_url = f"{str(driver.current_url)}"

        try:
            title = driver.find_element(By.XPATH, parent_box_xpath + "//h1").text
        except:
            title = None
        try:
            driver.find_element(
                By.XPATH, parent_box_xpath + '//span[text()="Temporarily closed"]'
            )
            is_temporarily_closed = True
        except:
            is_temporarily_closed = False
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
                    parent_box_xpath
                    + '//button[starts-with(@aria-label,"Plus code: ")]',
                )
                .get_attribute("aria-label")
                .replace("Plus code: ", "")
            )
        except:
            plus_code = None
        dict_array.append(
            {
                "source_url": url,
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
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    parent_box_xpath
                    + "/..//div[3]/span/button//*[local-name()='svg']/..",
                )
            )
        )
        driver.execute_script(
            "arguments[0].click()",
            driver.find_element(
                By.XPATH,
                parent_box_xpath + "/..//div[3]/span/button//*[local-name()='svg']/..",
            ),
        )
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element(
                (
                    By.XPATH,
                    parent_box_xpath
                    + "/..//div[3]/span/button//*[local-name()='svg']/..",
                )
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


def scroll_to_first_element(driver):
    driver.execute_script(
        "arguments[0].scrollIntoView()",
        driver.find_elements(
            By.XPATH,
            '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]',
        )[0],
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
        time.sleep(3)
        if results < len(
            driver.find_elements(
                By.XPATH,
                '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]',
            )
        ):
            results = len(
                driver.find_elements(
                    By.XPATH,
                    '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]',
                )
            )
            break_condition = False
        else:
            try:
                driver.find_element(
                    By.XPATH,
                    """//*[text()="You've reached the end of the list."]""",
                )
                break_condition = True
            except:
                scroll_to_first_element(driver)
                time.sleep(2)
                scroll_to_last_element(driver)
                time.sleep(2)
                current_results = len(
                    driver.find_elements(
                        By.XPATH,
                        '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]',
                    )
                )
                if current_results > results:
                    results = current_results
                    break_condition = False
                else:
                    break_condition = False
                    epoch_time = int(time.time())
                    while True:
                        current_time = int(time.time())
                        scroll_to_last_element(driver)
                        time.sleep(2.5)
                        scroll_to_first_element(driver)
                        time.sleep(4)
                        scroll_to_last_element(driver)
                        time.sleep(3)
                        elapsed_time = datetime.fromtimestamp(
                            current_time
                        ) - datetime.fromtimestamp(epoch_time)
                        try:
                            driver.find_element(
                                By.XPATH,
                                """//*[text()="You've reached the end of the list."]""",
                            )
                            break_condition = True
                        except:
                            break_condition = False
                        if break_condition == True:
                            break
                        if current_results > results:
                            results = current_results
                            epoch_time = int(time.time())
                            break
                        elif current_results == results and elapsed_time.seconds > 15:
                            break_condition = True
                            break
                        break_condition = False
            if break_condition == True:
                break
    current_results = len(
        driver.find_elements(
            By.XPATH,
            '//div[@role="main"]/div/div/div[@data-js-log-root and not(@class)]',
        )
    )
    print("Total Results: ", current_results)


def main():
    urls = pd.read_csv("map_scrape_input.csv").links.tolist()
    driver = start_browser()
    dict_array = []
    for url in urls:
        driver.get(str(url).replace("?hl=en", "") + "?hl=en")

        load_all_elements(driver)
        headers_loop(driver, url, dict_array)
        pd.DataFrame(dict_array).to_csv("map_scrape_output (Backup).csv", index=False)
    pd.DataFrame(dict_array).to_csv("map_scrape_output.csv", index=False)
    driver.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(traceback.format_exc())
    print("############  Sequence Completed  ############")
