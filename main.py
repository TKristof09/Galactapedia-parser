
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
    paragraphs = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//section[@class='p-article__content']//div[@class='c-markdown-content']/p")))
    text = ""
    for p in paragraphs:
        text += p.text + "\n"
    driver.quit()
    return text




if __name__ == '__main__':
    title = sys.argv[1]
    cont = len(sys.argv) > 2 and sys.argv[2] == "--continue"
    articles = {}
    try:
        with open(ARTICLES_FILENAME, 'r') as f:
            articles = json.load(f)
    except FileNotFoundError:
        with open(ARTICLES_FILENAME, 'w') as f:
            json.dump({}, f, indent=4)
    if title not in articles or title == "*":
        with open(LINKS_FILENAME, 'r') as f_links:
            links = json.load(f_links)
            if title == "*":
                title = random.choice(list(links.keys()))
            if title not in articles:
                articles[title] = parse_link(links[title])
        with open(ARTICLES_FILENAME, 'w') as f:
            json.dump(articles, f, indent=4)
    article = articles[title]
    s = article.replace('“', ' ').replace("UEE", "U-E-E").replace(';', ',').encode("charmap", errors="ignore").decode("charmap", errors="ignore")
    l = len(s)
    if l > 4000:
        if cont:
            p = int(sys.argv[3])
            start = s.find("\n", 2000 * p, 3500 * p)
            if start == -1:
                start = s.find(".", 2000 * p, 3500 * p)
            end = s.find("\n", start + 2000, start + 3500)
            if end == -1:
                end = s.find(".", start + 2000, start + 3500)
            s = s[start:end]
            if end != -1 and start != -1:
                s = s + " Do you want me to continue?"
        else:
            end = s.find("\n", 2000, 3500)
            if end == -1:
                end = s.find(".", 2000, 3500)
            s = s[:end]
            s = s + " Do you want me to continue?"
    print(s)



