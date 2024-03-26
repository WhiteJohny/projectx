import requests
from bs4 import BeautifulSoup as bs

url=''

r = requests.get(url)

soup = bs(r.content, "html.parser")

article = soup.find("article")

news_title = article.find(class_ = "headline speakable").text

paywall = soup.find('div', class_ = "paywall")
text = ''

for p in paywall.findAll('p'):
    text += p.text + '\n'

print(news_title)
print(text)

#url = "https://edition.cnn.com/2024/03/06/politics/takeaways-super-tuesday/index.html"