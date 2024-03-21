import requests
from bs4 import BeautifulSoup as bs


def fox_result(url):
    try:
        r = requests.get(url)
    except Exception:
        return None

    soup = bs(r.content, "html.parser")

    article = soup.find("article")

    try:
        news_title = article.find(class_="headline speakable").text
        paywall = soup.find('div', class_="article-body")

        text = ''

        for p in paywall.findAll('p'):
            text += p.text + '\n'

        return news_title, text
    except AttributeError:
        return None


print(fox_result('sgdsgs'))