from __future__ import annotations
import requests
from bs4 import BeautifulSoup as bs


def links_parser(search: str) -> list[str] | list:  # возвращает список ссылок на 20 последних новостей, если дать поисковый запрос
    url = f"https://nypost.com/?s={search}&sf=week"
    links = []
    r = requests.get(url)

    soup = bs(r.content, "html.parser")
    articles = soup.findAll('h3', class_='story__headline headline headline--archive')
    for a in articles:
        links.append(a.findNext('a').get('href'))
        if len(links) == 10:
            break

    return links


def nyp_one_parser(url: str) -> str | None:  # возвращает заголовок и текс статьи, если дать ссылку на статью
    try:
        r = requests.get(url)
        soup = bs(r.content, "html.parser")
        article = soup.find("div", class_="single__content entry-content m-bottom")
        news_title = soup.find("h1").text
        text = ''
        for p in article.findAll('p'):
            if p.text:
                text += p.text + '\n'
    except Exception:
        return None

    return f'{news_title}\n{text}'


def nyp_many_parser(search: str) -> list[str]:
    news_list = []
    links = links_parser(search)

    for link in links:
        text = nyp_one_parser(link)
        if text is not None: news_list.append(text)

    return news_list
