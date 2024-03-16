import requests
from bs4 import BeautifulSoup as bs

url1 = "https://www.yahoo.com/news/trump-defeats-haley-in-nearly-every-super-tuesday-state-setting-stage-for-2024-rematch-with-biden-041531333.html"
url = "https://www.yahoo.com/lifestyle/comedian-nick-swardson-escorted-off-203804886.html"

r = requests.get(url)

soup = bs(r.content, "html.parser")

article = soup.find("div", class_="caas-body")

news_title = soup.find("h1").text

text = ''

for p in article.findAll('p'):
    if p.text:
        text += p.text + '\n'

print(news_title)
print(text)