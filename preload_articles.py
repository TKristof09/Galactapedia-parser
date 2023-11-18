import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random

import json

if len(sys.argv) > 1:
    force_refresh = sys.argv[1] == "--force-refresh"
else:
    force_refresh = False

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


errored_articles = 0
def parse_article(links, id):
    global errored_articles
    global articles
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920,500)
    count = 0
    for title, link in links.items():
        if title in articles and not force_refresh:
            continue
        if count % 10 == 0:
            with open(ARTICLES_FILENAME + str(count // 10), 'w') as f:
                print(f"Saving articles checkpoint {str(count // 10)}...")
                json.dump(articles, f, indent=4)
        try:
            driver.get(link)
            sleep(random.uniform(20.0, 35.0)) # sleep to avoid making too many requests to the website
            paragraphs = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//section[@class='p-article__content']//div[@class='c-markdown-content']/p")))
            text = ""
            for p in paragraphs:
                text += p.text + "\n"
            print(f"Thread #{id}: Loaded {title} from {link}")
            articles[title] = text
            count += 1
        except Exception as e:
            print(f"Thread #{id}: Error {repr(e)} loading {title} from {link}. Skipping...")
            errored_articles += 1
            continue
    driver.quit()

try:
    parse_article(links, 0)
except KeyboardInterrupt:
    print("Stopping...")

if errored_articles > 0:
    print(f"{errored_articles} articles couldn't be loaded (due to timeouts most likely), try running the script again.")
with open(ARTICLES_FILENAME, 'w') as f:
    print("Saving articles...")
    json.dump(articles, f, indent=4)
