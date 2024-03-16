import requests
from bs4 import BeautifulSoup as bs

url1 = "https://abcnews.go.com/International/wireStory/chinese-coast-guard-blocks-vessels-off-south-china-107795637"
url = "https://abcnews.go.com/International/israel-hamas-talks-cease-fire-hostage-deal-gaza-war/story?id=107801137"

r = requests.get(url)

soup = bs(r.content, "html.parser")

article = soup.find("div", class_="xvlfx ZRifP TKoO eaKKC bOdfO")

news_title = soup.find("h1").text

text = ''

for p in article.findAll('p'):
    if p.text:
        text += p.text + '\n'

print(news_title)
print(text)