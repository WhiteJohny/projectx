from __future__ import annotations
import requests
import json
from datetime import timedelta, datetime


def text_parser(search: str) -> list[list[str]]:  # По поисковому запросу возвращает последние 10 новостей за последние 7 дней
    url = f"https://newssearch.chinadaily.com.cn/rest/en/search?keywords={search}&sort=dp&page=0&curType=story&type=&channel=&source="
    r = requests.get(url)
    content = json.loads(r.text)
    articles = []
    cur_date = datetime.now()
    week_ago = cur_date - timedelta(7)
    for article in content['content']:
        articles.append(article)
    result = []
    for article in articles:
        art_date = datetime(int(article['url'][32:36]), int(article['url'][36:38]), int(article['url'][39:41]))
        if week_ago <= art_date <= cur_date:
            result.append([article['title'], article['plainText']])

    return result


# print(text_parser('Bridge'))
