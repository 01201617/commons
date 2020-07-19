from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#【1】login
browser = webdriver.Firefox()
browser.get('https://nostarch.com')

html_elem = browser.find_element_by_tag_name('html')
html_elem.send_keys(Keys.END)
html_elem.send_keys(Keys.HOME)

#elem = browser.find_element_by_id('NAVIAREA01')
#browser.find_element_by_xpath('//div[@id="navi01P"]/ul/li[2]').click()

#kokunaikabushiki_elem = browser.find_element_by_id('navi01P')


#kokunaikabushiki_elem = browser.find_element_by_id('navi01P')
#browser.find_element_by_xpath('//div[@id="link02M"]/ul/li[2]').click()
#print(type(browser.current_url))
#soup = bs4.BeautifulSoup(browser.current_url)
#kokunaikabushiki_elem = soup.select('#HEADER01')
#kokunaikabushiki_elem = browser.find_element_by_class_name("floatClear")
#print('############')
#print(kokunaikabushiki_elem)
#print('############')
#elem = browser.find_element_by_id("navi01P")
#print(elem)