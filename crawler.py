from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1920,500)

BASE_URL = "https://robertsspaceindustries.com/galactapedia/"
driver.get(BASE_URL)


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
    articles_list = driver.find_element_by_class_name("c-article-index__list").get_property("children")
    titles = [x.get_property('children')[0].text for x in articles_list]
    while "" in titles:
        print("Empty title, retrying...")
        articles_list = driver.find_element_by_class_name("c-article-index__list").get_property("children")
        titles = [x.get_property('children')[0].text for x in articles_list]
    letter = button.text[0]
    links[letter] = {}
    for article in articles_list:
        article_element = article.get_property('children')[0]
        links[letter][article_element.text] = article_element.get_property('href')
        
driver.close()


import json
with open("articles.json", 'w') as f:
    json.dump(links, f)