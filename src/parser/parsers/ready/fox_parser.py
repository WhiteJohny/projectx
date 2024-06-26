import requests
import time

from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.common.by import By

from src.model.model import model_imitation


def fox_search(search_query):
    browser = webdriver.Chrome()
    browser.maximize_window()

    browser.get(f"https://www.foxnews.com/search-results/search?q={search_query}")

    select = browser.find_element(By.CLASS_NAME, "select")
    select.click()

    select_article = browser.find_element(By.XPATH, "//*[@id='wrapper']/div[2]/div[1]/div/div[2]/div[2]/ul/li["
                                                    "1]/label/input")
    select_article.click()
    select.click()

    month_min = '//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div[3]/div[1]/div[1]/button'
    date_min = '//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div[3]/div[1]/div[2]/button'
    year_min = '//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div[3]/div[1]/div[3]/button'
    month_max = '//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[1]/button'
    date_max = '//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[2]/button'
    year_max = '//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[3]/button'

    mmin_b = browser.find_element(By.XPATH, month_min)
    mmin_b.click()
    m1 = browser.find_element(By.XPATH, '//*[@id="03"]')
    m1.click()
    time.sleep(1)
    dmin_b = browser.find_element(By.XPATH, date_min)
    dmin_b.click()
    d1 = browser.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[1]/div/div[2]/div[3]/div[1]/div[2]/ul/li[1]')
    d1.click()
    time.sleep(1)
    ymin_b =  browser.find_element(By.XPATH, year_min)
    ymin_b.click()
    y1 = browser.find_element(By.XPATH, '//*[@id="2024"]')
    y1.click()
    time.sleep(1)
    mmax_b = browser.find_element(By.XPATH, month_max)
    mmax_b.click()
    m2 = browser.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[1]/ul/li[3]')
    m2.click()
    time.sleep(1)
    dmax_b = browser.find_element(By.XPATH, date_max)
    dmax_b.click()
    d2 = browser.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[2]/ul/li[10]')
    d2.click()
    time.sleep(1)
    ymax_b = browser.find_element(By.XPATH, year_max)
    ymax_b.click()
    y2 = browser.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[3]/ul/li[1]')
    y2.click()
    time.sleep(1)

    search_button = browser.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/div[1]/div/div[1]/div[2]/div/a')
    search_button.click()
    time.sleep(5)

    while True:
        try:
            loadmore_button = browser.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/div[2]/div/div[3]/div[2]/a/span')
            loadmore_button.click()
            time.sleep(2)
        except Exception:
            break
    time.sleep(5)

    source_data = browser.page_source
    soup = bs(source_data, features="html.parser")

    articles = soup.findAll("h2", class_="title")

    links = []

    for a in articles:
        links.append(a.findNext('a').get('href'))

    time.sleep(5)
    browser.close()

    return links


def fox_result(url):
    try:
        r = requests.get(url)
    except Exception:
        return None

    soup = bs(r.content, "html.parser")

    article = soup.find("article")

    try:
        news_title = article.find(class_="headline speakable").text
        paywall = soup.find('div', class_="article-body")

        text = ''

        for p in paywall.findAll('p'):
            text += p.text + '\n'

        return [news_title, text]
    except AttributeError:
        return None


def fox_many_parser(search_query):
    news_list = []

    links = fox_search(search_query)

    for link in links:
        news_list.append(fox_result(link))

    return model_imitation(news_list)


def fox_one_parser(url):
    text = fox_result(url)

    if text is None:
        return "Ваша ссылка недействительна или она не с foxnews"

    return "Это позитивная новость!" if model_imitation([text])[:3] == '100' else "Это печальная новость("
