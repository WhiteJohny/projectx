import requests
from bs4 import BeautifulSoup as bs

url1 = "https://www.nbcnews.com/politics/politics-news/georgia-republicans-issue-subpoena-probe-fani-willis-rcna141960"
url = "https://www.nbcnews.com/politics/2024-election/california-senate-primary-win-election-rcna141271"

r = requests.get(url)

soup = bs(r.content, "html.parser")

article = soup.find("div", class_="article-body__content")

news_title = soup.find("h1").text

text = ''

for p in article.findAll('p'):
    if p.text:
        text += p.text + '\n'

print(news_title)
print(text)