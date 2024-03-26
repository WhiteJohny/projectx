import requests
from bs4 import BeautifulSoup as bs

url1 = "https://www.huffpost.com/entry/minnesota-uncommitted-nikki-haley-vermont-super-tuesday-2024_n_65e80917e4b0170871fc1556"
url = "https://www.huffpost.com/entry/nikki-haley-wins-vermont-republican-primary_n_65e7e8e0e4b0d2a2475b126f"

r = requests.get(url)

soup = bs(r.content, "html.parser")

article = soup.findAll("div", class_="primary-cli cli cli-text")

news_title = soup.find("h1").text

text = ''

for p in article:
    if p.text:
        text += p.text + '\n'

print(news_title)
print(text)