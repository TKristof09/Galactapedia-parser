
import sys
import json
from bs4 import BeautifulSoup
import requests

FILENAME = "articles.json"
class Card:
    def __init__(self, image, table):
        self.image = image
        self.table = table
        
class Article:
    def __init__(self, text, categories, tags, card):
        self.text = text
        self.categories = categories
        self.tags = tags
        self.card = card
        
def parse_article(title):
    links = {}
    with open(FILENAME, 'r') as f:
        links = json.load(f)
    first_letter = title[0]
    if first_letter.isdigit():
        first_letter = "#"
    url = links[first_letter][title]
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="lxml")

    categories_base_url = "https://https://robertsspaceindustries.com"
    cat_ul = soup.find('ul', class_="p-article__categories")
    if cat_ul is not None:
        categories = [(x.text, categories_base_url + x.a["href"]) for x in cat_ul.children]

    tags_base_url = "https://https://robertsspaceindustries.com"
    tags_ul = soup.find('ul', class_="p-article__tags")
    if tags_ul is not None:
        tags = [(x.text, tags_base_url + x.a["href"]) for x in tags_ul.children]

    md = soup.find('section', class_="p-article__content").find("div", class_="c-markdown-content")
    text = ""
    for i in md.children:
        text += i.text +" : "

    card = soup.find("div", class_="c-card")
    if card is not None:
        image = card.find("figure", class_="c-card__image").img["src"]

    table = {}
    table_ul = card.find("ul", class_="c-table")
    if table_ul is not None:
        for i in table_ul.children:
            cells = list(i.children)
            table[cells[0].text] = cells[1].text
    
    return Article(text, categories, tags, Card(image, table))
if __name__ == '__main__':
        title = sys.argv[1]
        article = parse_article(title)
        print(article.text.replace("UEE", "U-E-E").replace("’", "'").replace(';', ',').encode("charmap", errors="ignore").decode("charmap", errors="ignore"))
