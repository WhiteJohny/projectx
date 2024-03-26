import requests
from bs4 import BeautifulSoup as bs

url2 = "https://www.foxnews.com/politics/republican-presidential-candidate-ryan-binkley-drops-out-endorses-trump"
url1 = "https://www.foxnews.com/politics/super-tuesday-expected-boost-trump-closer-clinching-gop-nomination-haley-makes-possible-last-stand"
url = "https://www.foxnews.com/politics/trump-reacts-super-tuesday-victories-rarely-has-politics-seen-anything-quite-like-this"

r = requests.get(url)

soup = bs(r.content, "html.parser")

article = soup.find("article")

news_title = article.find(class_="headline speakable").text

paywall = soup.find('div', class_="article-body")
text = ''

for p in paywall.findAll('p'):
    text += p.text + '\n'

print(news_title)
print(text)
