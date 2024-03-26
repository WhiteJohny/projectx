from __future__ import annotations
import requests
from bs4 import BeautifulSoup as bs

def links_parser(search: str) -> list:   #возвращает список ссылок на 20 последних новостей, если дать поисковый запрос
    url = f"https://www.rt.com/search?q={search}"
    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    links = []
    articles = soup.findAll('div', class_="list-card__content--title link_hover")
    for a in articles:
        links.append('https://www.rt.com' + a.findNext('a').get('href'))

    return links

def text_parser(url: str) -> list(str):                                    #возвращает заголовок и текс статьи, если дать ссылку на статью
    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    article = soup.find("div", class_="article__text")
    news_title = soup.find("h1").text
    text = ''
    for p in article.findAll('p'):
        if p.text:
            text += p.text + '\n'

    return [news_title, text]

for link in links_parser('Trump'):
    print(text_parser(link))