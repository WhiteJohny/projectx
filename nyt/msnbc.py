import requests
from bs4 import BeautifulSoup as bs

url1 = "https://www.msnbc.com/rachel-maddow-show/maddowblog/gops-ernst-wants-stop-biden-delivering-state-union-rcna141821"
url = "https://www.msnbc.com/deadline-white-house/deadline-legal-blog/supreme-court-trump-ballot-immunity-timing-rcna141839"

r = requests.get(url)

soup = bs(r.content, "html.parser")

article = soup.find("div", class_="showblog-body__content")

news_title = soup.find("h1").text

text = ''

for p in article.findAll('p'):
    if p.text:
        text += p.text + "\n"

print(news_title)
print(text)