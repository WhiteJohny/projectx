import requests
from bs4 import BeautifulSoup as bs

search = 'Trump'
url = f"https://abcnews.go.com/search?searchtext={search}&after=week&type=Story"
url2 = f"https://abcnews.go.com/search?searchtext={search}&after=week&type=Story&page=2"

r = requests.get(url)

soup = bs(r.text, "html.parser")
links = []
roll = soup.find("div", class_="Search__body__wrapper w-100")
articles = roll.findAll("a")
print(articles)