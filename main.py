
import sys
import json
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

LINKS_FILENAME = "links.json"
ARTICLES_FILENAME = "articles.json"

def parse_link(link):

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(700,500)
    driver.get(link)
    article = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//section[@class='p-article__content']//div[@class='c-markdown-content']")))
    text = ""
    for p in article.get_property("children"):
        text += p.text + "\n"
    driver.quit()
    return text


def parse_article(title):
    articles = {}
    with open(FILENAME, 'r') as f:
        articles = json.load(f)
    return articles[title]

if __name__ == '__main__':
    title = sys.argv[1]
    articles = {}
    try:
        with open(ARTICLES_FILENAME, 'r') as f:
            articles = json.load(f)
    except FileNotFoundError:
        with open(ARTICLES_FILENAME, 'w') as f:
            f.write(json.dumps({}))
    if title not in articles or title == "*":
        with open(LINKS_FILENAME, 'r') as f_links:
            links = json.load(f_links)
            if title == "*":
                title = random.choice(list(links.keys()))
            if title not in articles:
                articles[title] = parse_link(links[title])
        with open(ARTICLES_FILENAME, 'w') as f:
            f.write(json.dumps(articles))
    article = articles[title]
    #article = parse_article(title)
    print(article.replace('“', ' ').replace("UEE", "U-E-E").replace(';', ',').encode("charmap", errors="ignore").decode("charmap", errors="ignore")[:-1])



