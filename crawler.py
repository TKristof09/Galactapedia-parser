from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import threading

chrome_options = Options()
#@chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1920,500)

BASE_URL = "https://robertsspaceindustries.com/galactapedia/"
driver.get(BASE_URL)


try:
    cookie_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "allow-selected")))
    print(cookie_button)
    cookie_button.click()
except TimeoutException as e:
    pass

categories_button, tags_button, index_button = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "c-tabs__title")))

index_button.click()
letter_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "c-article-index__nav-button")))

links = {}
for button in letter_buttons:
    print(button.text[0])
    if not button.is_displayed():
        print("Scrolling...")
        x,y = button.location
        driver.execute_script(f"window.scrollTo({x},{y})")
    if button.is_enabled():
        button.click()
    else:
        continue
    articles_list = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//ul[@class='c-article-index__list']/li")))
    titles = [x.get_property('children')[0].text for x in articles_list]
    for article in articles_list:
        article_element = article.get_property('children')[0]
        links[article_element.text] = article_element.get_property('href')
        print(f"{article_element.text} to {article_element.get_property('href')}")

driver.close()

import json
with open("links.json", 'w') as f:
    json.dump(links, f, indent=4)

