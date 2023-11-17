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
    json.dump(links, f)

"""
def split(d, chunks):
    chunk_len = len(d) // (chunks + 1)
    chunks_list = []
    count = 0
    for title, link in d.items():
        if count % chunk_len == 0:
            chunks_list.append({})
        chunks_list[-1][title] = link
        count += 1
    return chunks_list

articles = {}
def parse_article(links):
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920,500)
    for title, link in links.items():
        driver.get(link)
        article = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//section[@class='p-article__content']//div[@class='c-markdown-content']")))
        text = article.get_property("children")[0].text
        articles[title] = text
    driver.quit()

threads = []
for l in split(links, 1):
    th = threading.Thread(target=parse_article, args=(l,))
    th.start() # could `time.sleep` between 'clicks' to see whats'up without headless option
    threads.append(th)
for th in threads:
    th.join() # Main thread wait for threads finish


import json
with open("articles.json", 'w') as f:
    json.dump(articles, f)
"""
