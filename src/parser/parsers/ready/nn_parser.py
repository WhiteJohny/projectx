from __future__ import annotations
import requests
from bs4 import BeautifulSoup as bs

from src.model.model import model_imitation


def links_parser(search: str) -> list[str] | list:  # возвращает список ссылок на 20 последних новостей, если дать поисковый запрос
    url = f"https://www.newsinlevels.com/?s={search}"
    links = []

    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    articles = soup.findAll('div', class_="title")

    for a in articles:
        links.append(a.findNext('a').get('href'))

    if links:
        url2 = f"https://www.newsinlevels.com/page/2/?s={search}"

        r = requests.get(url2)
        soup = bs(r.content, "html.parser")
        articles = soup.findAll('div', class_="title")

        for a in articles:
            links.append(a.findNext('a').get('href'))

    return links


def text_parser(url: str) -> list[str, str] | list:  # возвращает заголовок и текс статьи, если дать ссылку на статью
    try:
        r = requests.get(url)
        soup = bs(r.content, "html.parser")
        article = soup.find("div", id="nContent")
        news_title = soup.find("h2").text

        text = ''
        for p in article.findAll('p'):
            if p.text:
                text += p.text + '\n'
    except Exception:
        return []

    return [news_title, text]


def nn_one_parser(url: str) -> str:
    try:
        news_title, text = text_parser(url)
        all_text = f'{news_title}\n{text}'
    except ValueError:
        all_text = None

    if all_text is None:
        return "Ваша ссылка недействительна или она не с nn"

    return "Это позитивная новость!" if model_imitation([all_text])[:3] == '100' else "Это печальная новость("


def nn_many_parser(search: str) -> str:
    news_list = []
    links = links_parser(search)

    for link in links:
        news_title, text = text_parser(link)
        news_list.append(f'{news_title}\n{text}')

    return model_imitation(news_list)
