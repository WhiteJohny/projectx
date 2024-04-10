from __future__ import annotations
import requests
from bs4 import BeautifulSoup as bs

from src.model.model import model_imitation


def links_parser(search: str) -> list:  # возвращает список ссылок на 20 последних новостей, если дать поисковый запрос
    url = f"https://nypost.com/search/{search}/"
    links = []

    try:
        r = requests.get(url)
        soup = bs(r.content, "html.parser")
        articles = soup.findAll('h3', class_='story__headline headline headline--archive')

        for a in articles:
            links.append(a.findNext('a').get('href'))
    except Exception:
        return []

    return links


def text_parser(url: str) -> list[str, str]:  # возвращает заголовок и текс статьи, если дать ссылку на статью
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
        return []

    return [news_title, text]


def nyp_one_parser(url: str) -> str:
    try:
        news_title, text = text_parser(url)
        all_text = f'{news_title}\n{text}'
    except ValueError:
        all_text = None

    if all_text is None:
        return "Ваша ссылка недействительна или она не с nyp"

    return "Это позитивная новость!" if model_imitation([all_text])[:3] == '100' else "Это печальная новость("


def nyp_many_parser(search: str) -> str:
    news_list = []
    links = links_parser(search)

    for link in links:
        news_title, text = text_parser(link)
        news_list.append(f'{news_title}\n{text}')

    return model_imitation(news_list)
