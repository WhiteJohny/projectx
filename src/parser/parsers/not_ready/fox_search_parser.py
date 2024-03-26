# from selenium import webdriver
# import time
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup as bs
# from datetime import timedelta, datetime
#
# cur_date = datetime.now()
# cur_month = str(cur_date)[5:7]
# cur_day = str(cur_date)[8:10]
#
# week_ago = cur_date - timedelta(7)
# week_year = str(week_ago)[:4]
# week_month = str(week_ago)[5:7]
# week_day = str(week_ago)[8:10]
#
# browser = webdriver.Chrome()
# browser.maximize_window()
#
# search_query = 'Trump'
# browser.get(f"https://www.foxnews.com/search-results/search?q={search_query}")
#
# select = browser.find_element(By.CLASS_NAME, "select")
# select.click()
#
# select_article = browser.find_element(By.XPATH, "//*[@id='wrapper']/div[2]/div[1]/div/div[2]/div[2]/ul/li["
#                                                 "1]/label/input")
# select_article.click()
# select.click()
#
# <<<<<<< HEAD:src/parser/parsers/nw/fox_search_parser.py
# #кнопки для выбора даты
# month_min ='//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div[3]/div[1]/div[1]/button'
# =======
# month_min = '//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div[3]/div[1]/div[1]/button'
# >>>>>>> 280a5c381c1bc5648557ff1399f1ae145a69a500:src/parser/parsers/fox_search_parser.py
# date_min = '//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div[3]/div[1]/div[2]/button'
# year_min = '//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div[3]/div[1]/div[3]/button'
# month_max = '//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[1]/button'
# date_max = '//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[2]/button'
# year_max = '//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[3]/button'
#
# mmin_b = browser.find_element(By.XPATH, month_min)
# mmin_b.click()
# m1 = browser.find_element(By.XPATH, f'//*[@id="{week_month}"]')
# m1.click()
# time.sleep(1)
# dmin_b = browser.find_element(By.XPATH, date_min)
# dmin_b.click()
# d1 = browser.find_element(By.XPATH, f'/html/body/div/div/div/div[2]/div[1]/div/div[2]/div[3]/div[1]/div[2]/ul/li[{week_day}]')
# d1.click()
# time.sleep(1)
# ymin_b =  browser.find_element(By.XPATH, year_min)
# ymin_b.click()
# y1 = browser.find_element(By.XPATH, f'//*[@id="{week_year}"]')
# y1.click()
# time.sleep(1)
# mmax_b = browser.find_element(By.XPATH, month_max)
# mmax_b.click()
# m2 = browser.find_element(By.XPATH, f'/html/body/div/div/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[1]/ul/li[{cur_month}]')
# m2.click()
# time.sleep(1)
# dmax_b = browser.find_element(By.XPATH, date_max)
# dmax_b.click()
# d2 = browser.find_element(By.XPATH, f'/html/body/div/div/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[2]/ul/li[{cur_day}]')
# d2.click()
# time.sleep(1)
# ymax_b = browser.find_element(By.XPATH, year_max)
# ymax_b.click()
# y2 = browser.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[3]/ul/li[1]')
# y2.click()
# time.sleep(1)
#
# search_button = browser.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/div[1]/div/div[1]/div[2]/div/a')
# search_button.click()
# time.sleep(5)
#
# while True:
#     try:
#         loadmore_button = browser.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/div[2]/div/div[3]/div[2]/a/span')
#         loadmore_button.click()
#         time.sleep(2)
#     except Exception:
#         break
# time.sleep(5)
#
# source_data = browser.page_source
# soup = bs(source_data, features="html.parser")
#
# articles = soup.findAll("h2", class_="title")
# links = []
# for a in articles:
#     links.append(a.findNext('a').get('href'))
# print(links)
#
# time.sleep(5)
# browser.close()
