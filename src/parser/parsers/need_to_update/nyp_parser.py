from __future__ import annotations
import requests
from bs4 import BeautifulSoup as bs


def links_parser(search: str) -> list:  # Возвращает список ссылок на 20 последних новостей, если дать поисковый запрос
    url = f"https://nypost.com/?s={search}&sf=week"
    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    links = []
    articles = soup.findAll('h3', class_='story__headline headline headline--archive')
    for a in articles:
        links.append(a.findNext('a').get('href'))
        if len(links) == 10:
            break

    return links


def text_parser(url: str) -> list[str]:  # Возвращает заголовок и текс статьи, если дать ссылку на статью
    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    article = soup.find("div", class_="single__content entry-content m-bottom")
    news_title = soup.find("h1").text
    text = ''
    for p in article.findAll('p'):
        if p.text:
            text += p.text + '\n'

    return [news_title, text]


# for link in links_parser('Egg'):
#     print(text_parser(link))
