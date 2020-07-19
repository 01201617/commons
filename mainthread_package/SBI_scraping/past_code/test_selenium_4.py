from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://mail.yahoo.com')
#browser.get('https://login.yahoo.co.jp/config/login?.src=ym&.done=https%3A%2F%2Fmail.yahoo.co.jp')
email_elem = browser.find_element_by_id('login-username')
#メールアドレスを記入してEnter
email_elem.send_keys('test_saibino4ban@yahoo.com')
email_elem.submit()
#なぜかこっから下は動かない
password_elem = browser.find_element_by_id('login-passwd')
password_elem.send_keys('12345SQL')
password_elem.submit()