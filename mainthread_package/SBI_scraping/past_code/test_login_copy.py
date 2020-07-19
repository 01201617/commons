from selenium import webdriver
import bs4
import requests

url = 'https://www.sbisec.co.jp/ETGate'
res = requests.get(url)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text)
kokunaikabushiki_elem = soup.select('#user_input')
print('fin')
print(kokunaikabushiki_elem)
#elem = browser.find_element_by_id("navi01P")
#print(elem)