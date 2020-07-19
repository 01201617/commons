import csv
import sys
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#【1】login
def login(browser):
    browser.get('https://www.sbisec.co.jp/ETGate')

    browser.find_element_by_name("user_id").send_keys("AAA")
    browser.find_element_by_name("user_password").send_keys("AAA")
    browser.find_element_by_name("ACT_login").click()

#【2】frameまでページ遷移
def transit_page():
    """目的ページまで遷移"""
    #↓ <a>要素に挟まれていたら、link_textで簡単に指定できる
    browser.implicitly_wait(10)
    browser.find_element_by_link_text('国内株式').click()
    browser.implicitly_wait(10)
    browser.find_element_by_link_text('スクリーニング').click()
    browser.implicitly_wait(10)


    ## ↓ダメだったコードたち…
    #↓松やつ…でもダメでした
    # WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it(
    #      (By.XPATH,"//*[@id='middleAreaMScr']/table/tbody/tr[2]/td/div/iframe")))

    # browser.find_element_by_css_selector("#root > div > div > div.criteriapane > div > div.SearchBoxTop > div").click()
    # browser.switch_to.default_content()
    # WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it(
    #     (By.CSS_SELECTOR,"body > table > tbody > tr:nth-child(212) > td.line-content > span:nth-child(2) > a")))
    # iframe = browser.find_element_by_css_selector("body > table > tbody > tr:nth-child(212) > td.line-content > span:nth-child(2) > a")
    # browser.switch_to.frame(iframe)
    # browser.implicitly_wait(10)
    # browser.find_element_by_id("root").click()


    # frame = browser.find_element_by_tag_name("iframe")
    # Elementもしくは、id, nameの指定が可能
    # browser.find_element_by_id("root").click()
    # browser.find_element_by_css_selector("#searchbtn").click()
    # # browser.find_element_by_id("#検索").click()
    # # browser.find_element_by_css_selector("#root > div > div > div.criteriapane > div > div.SearchBoxTop > div")
    # # browser.find_element_by_xpath("/html/body/div/div/div/div[6]/div/div[2]/div").click()
    # # browser.find_element_by_class_name('Myスクリーナー').click()
    # # browser.find_element_by_link_text('Myスクリーナー').click()
    # browser.implicitly_wait(10)
    # browser.find_element_by_link_text('Dailycheck').click()
#【3】frame遷移
def transit_frame():
    """frame遷移がどうしてもできなかったので、属性からurl取得して、再度、入り直した！！"""
    iframe = browser.find_element_by_xpath("//*[@id='middleAreaMScr']/table/tbody/tr[2]/td/div/iframe").get_attribute("src")
    browser.get(iframe)
    browser.implicitly_wait(10)

#【4】table選択+csvダウンロード
def get_csv():
    """frame内のtableを、目的通り選択し、csvダウンロードをクリックする。"""
    # ↓複雑なので、基本、css or Xpathで取得 Todo 検証->Copy css, xpath　か、 seleniumuIDEでマクロ記録の様にコードが簡単にわかる!!
    browser.find_element_by_css_selector("#root > div > div > div:nth-child(2) > div.CriteriaListWidget > div > div.toggleresult > label > div > div.react-switch-bg")
    # browser.find_element(By.CSS_SELECTOR, ".react-switch-bg").click()

    browser.find_element_by_xpath("//*[@id='root']/div/div/div[6]/div/div[2]/div").click()
    browser.find_element(By.CSS_SELECTOR, ".selectallmini > .name").click()
    browser.find_element(By.CSS_SELECTOR,
                             ".innerCollapsible:nth-child(1) .SelectionBox:nth-child(1) > .name").click()
    browser.find_element(By.CSS_SELECTOR,
                             ".innerCollapsible:nth-child(2) .SelectionBox:nth-child(1) > .name").click()

    browser.find_element_by_xpath("//*[@id='root']/div/div/div[5]/div[2]/div[3]/div").click()


def get_current_html(browser):
    """現在ページのhtmlを表示するコード"""
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    html = soup.prettify()
    print(html)

if __name__=="__main__":

    browser = webdriver.Chrome()

    #[1]ログイン
    login(browser)

    # 【2】tableまでページ遷移
    transit_page()

    # 【3】frame遷移
    transit_frame()

    # 【4】table選択+csvダウンロード
    get_csv()

    print('fin')

    #現在ページのhtmlを表示するコード
    # get_current_html(browser)