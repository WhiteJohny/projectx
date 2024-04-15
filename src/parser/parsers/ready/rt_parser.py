from __future__ import annotations

import requests

from bs4 import BeautifulSoup as bs
from datetime import timedelta, datetime

from src.model.model import model_imitation


def links_parser(search: str) -> list:  # возвращает список ссылок на 20 последних новостей, если дать поисковый запрос
    url = f"https://www.rt.com/search?q={search}&type=News"
    months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07',
              'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    links = []

    try:
        r = requests.get(url)
        soup = bs(r.content, "html.parser")

        cur_date = datetime.now()
        week_ago = cur_date - timedelta(7)
        articles = soup.findAll('div', class_="list-card__content")

        for a in articles:
            month, day, year = a.find('span', class_="date").text[:-8].split()
            art_date = datetime(int(year), int(f'{months[month]}'), int(day[:-1]))
            if week_ago <= art_date <= cur_date:
                links.append('https://www.rt.com' + a.findNext('a').get('href'))
    except Exception:
        return []

    return links


def text_parser(url: str) -> list[str, str] | list:  # возвращает заголовок и текс статьи, если дать ссылку на статью
    try:
        r = requests.get(url)
        soup = bs(r.content, "html.parser")
        article = soup.find("div", class_="article__text")
        news_title = soup.find("h1").text
        text = ''
        for p in article.findAll('p'):
            if p.text:
                text += p.text + '\n'
    except Exception:
        return []

    return [news_title, text]


def rt_one_parser(url: str) -> str:
    try:
        news_title, text = text_parser(url)
        all_text = f'{news_title}\n{text}'
    except ValueError:
        all_text = None

    if all_text is None:
        return "Ваша ссылка недействительна или она не с rt"

    return "Это позитивная новость!" if model_imitation([all_text])[:3] == '100' else "Это печальная новость("


def rt_many_parser(search: str) -> str:
    news_list = []
    links = links_parser(search)

    for link in links:
        news_title, text = text_parser(link)
        news_list.append(f'{news_title}\n{text}')

    return model_imitation(news_list)
