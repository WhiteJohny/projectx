from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs

browser = webdriver.Chrome()
# browser.maximize_window()

search_query = 'Trump'
browser.get(f"https://www.foxnews.com/search-results/search?q={search_query}")
loadmore_button = browser.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/div[2]/div/div[3]/div[2]/a/span')
loadmore_button.click()
time.sleep(5)
source_data = browser.page_source
soup = bs(source_data, features="html.parser")

articles = soup.findAll("h2", class_="title")
links = []
for a in articles:
    links.append(a.findNext('a').get('href'))
print(links)
# articles = browser.find_elements(By.CSS_SELECTOR, 'h2.title')
# for article in articles[2:]:
#     print(article.get_attribute('href'))

browser.close()