from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import threading
from time import sleep
import random

import json

LINKS_FILENAME = "links.json"
ARTICLES_FILENAME = "articles.json"

links = {}
articles = {}
with open(LINKS_FILENAME, 'r') as f_links:
    links = json.load(f_links)

try:
    with open(ARTICLES_FILENAME, 'r') as f:
        articles = json.load(f)
except FileNotFoundError:
    with open(ARTICLES_FILENAME, 'w') as f:
        f.write(json.dumps({}))


def split(d, chunks):
    chunk_len = len(d) // chunks + 1
    chunks_list = []
    count = 0
    for title, link in d.items():
        if count % chunk_len == 0:
            chunks_list.append({})
        chunks_list[-1][title] = link
        count += 1
    return chunks_list

stop = False
def parse_article(links, id):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920,500)
    for title, link in links.items():
        if stop:
            break
        if title in articles:
            continue
        try:
            driver.get(link)
            print(f"Thread #{id}: Loading {title} from {link}")
            sleep(random.uniform(1.0, 7.0)) # sleep to avoid making too many requests to the website
            article = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//section[@class='p-article__content']//div[@class='c-markdown-content']")))
            text = article.get_property("children")[0].text
            articles[title] = text
        except Exception as e:
            break
    driver.quit()

threads = []
for l in split(links, 2):
    th = threading.Thread(target=parse_article, args=(l,len(threads)))
    th.start() # could `time.sleep` between 'clicks' to see whats'up without headless option
    threads.append(th)
try:
    for th in threads:
        th.join() # Main thread wait for threads finish
except KeyboardInterrupt:
    print("Stopping...")
    stop = True
    for th in threads:
        th.join() # Main thread wait for threads finish



import json
with open(ARTICLES_FILENAME, 'w') as f:
    json.dump(articles, f)
