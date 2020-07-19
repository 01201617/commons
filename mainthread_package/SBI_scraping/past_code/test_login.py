from selenium import webdriver
import bs4

#【1】login
browser = webdriver.Firefox()
browser.get('https://www.sbisec.co.jp/ETGate')

browser.find_element_by_name("user_id").send_keys("305-0285692")
browser.find_element_by_name("user_password").send_keys("KaNT#1617")
browser.find_element_by_name("ACT_login").click()
