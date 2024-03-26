from __future__ import annotations
import requests
from bs4 import BeautifulSoup as bs

def links_parser(search: str) -> list:                 #возвращает список ссылок на 20 последних новостей, если дать поисковый запрос
    url = f"https://www.newsinlevels.com/?s={search}"
    links = []
    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    articles = soup.findAll('div', class_="title")
    for a in articles:
        links.append(a.findNext('a').get('href'))
    url2 = f"https://www.newsinlevels.com/page/2/?s={search}"
    r = requests.get(url2)
    soup = bs(r.content, "html.parser")
    articles = soup.findAll('div', class_="title")
    for a in articles:
        links.append(a.findNext('a').get('href'))

    return links

def text_parser(url: str) -> list(str):                                    #возвращает заголовок и текс статьи, если дать ссылку на статью
    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    article = soup.find("div", id="nContent")
    news_title = soup.find("h2").text
    text = ''
    for p in article.findAll('p'):
        if p.text:
            text += p.text + '\n'

    return [news_title, text]

for link in links_parser('Trump'):
    print(text_parser(link))
