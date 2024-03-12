import requests
from bs4 import BeautifulSoup as bs

search = 'Trump'
url = f"https://abcnews.go.com/search?searchtext={search}&after=week"

print(url)