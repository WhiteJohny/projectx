from __future__ import annotations
import requests
import json

from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
from datetime import timedelta, datetime


def chinadaily_many_parser(search: str) -> list[str]:  # По поисковому запросу возвращает последние 10 новостей за последние 7 дней
    url = f"https://newssearch.chinadaily.com.cn/rest/en/search?keywords={search}&sort=dp&page=0&curType=story&type=&channel=&source="
    articles = []
    result = []
    try:
        r = requests.get(url)
        content = json.loads(r.text)
        cur_date = datetime.now()
        week_ago = cur_date - timedelta(7)

        for article in content['content']:
            articles.append(article)

        for article in articles:
            art_date = datetime(int(article['url'][32:36]), int(article['url'][36:38]), int(article['url'][39:41]))
            if week_ago <= art_date <= cur_date:
                if article['plainText'] is not None and article['plainText'] != "":
                    result.append(f"{article['title']}\n{article['plainText']}")
    except Exception:
        pass

    return result


def chinadaily_one_parser(url: str) -> str | None:
    try:
        session = HTMLSession()
        r = session.get(url)
        soup = bs(r.text, 'html.parser')

        if soup.find("span", class_="pageno"):
            pages = soup.find("span", class_="pageno")
            page = ''.join(pages.text.split())
            text = ''
            for i in range(int(page[2:])):
                r = session.get(url[:-6]+f'{i+1}.html')
                soup = bs(r.text, 'html.parser')
                article = soup.find("div", id="Content")
                for p in article.findAll('p'):
                    if p.text:
                        text += p.text + '\n'
            news_title = soup.find("h1").text
        else:
            article = soup.find("div", id="Content")
            news_title = soup.find("h1").text
            text = ''
            for p in article.findAll('p'):
                if p.text:
                    text += p.text + '\n'
    except Exception:
        return None

    return f'{news_title}\n{text}'
