from __future__ import annotations
import requests
from bs4 import BeautifulSoup as bs
from datetime import timedelta, datetime


def links_parser(search: str) -> list:  # Возвращает список ссылок на 20 последних новостей, если дать поисковый запрос
    url = f"https://www.rt.com/search?q={search}&type=News"
    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
              'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    cur_date = datetime.now()
    week_ago = cur_date - timedelta(7)
    links = []
    articles = soup.findAll('div', class_="list-card__content")
    for a in articles:
        month, day, year = a.find('span', class_="date").text[:-8].split()
        art_date = datetime(int(year), int(f'{months[month]}'), int(day[:-1]))
        if week_ago <= art_date <= cur_date:
            links.append('https://www.rt.com' + a.findNext('a').get('href'))

    return links


def text_parser(url: str) -> list[str]:  # Возвращает заголовок и текст статьи, если дать ссылку на статью
    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    article = soup.find("div", class_="article__text")
    news_title = soup.find("h1").text
    text = ''
    for p in article.findAll('p'):
        if p.text:
            text += p.text + '\n'

    return [news_title, text]


# for link in links_parser('Bridge'):
#     print(text_parser(link))
