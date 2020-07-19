from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://inventwithpython.com')

#link_elem = browser.find_element_by_link_text('Read It Online')

# More Infoという値(text)を含むエレメントを取得(はじめの一つ)
# →ここでは、それはhref属性値をもつ<a>要素である。(クリックできる。)
link_elem = browser.find_element_by_link_text('More Info')
print(link_elem.text)
print(type(link_elem))
link_elem.click()