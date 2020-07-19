import csv
import sys
#正規表現用のモジュール
import re

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

sys.setrecursionlimit(3000)  # 再帰リミット(リストのリスト、ネストの回数)を1001に設定


#【1】login
def login(browser):
    browser.get('https://www.sbisec.co.jp/ETGate')

    browser.find_element_by_name("user_id").send_keys("305-0285692")
    browser.find_element_by_name("user_password").send_keys("KaNT#1617")
    browser.find_element_by_name("ACT_login").click()

#【2】国内株式のリンクをクリック

def data_get_initial(stock_code):

    # 要素が見つかるまで10秒待つ設定
    browser.implicitly_wait(10) # seconds

    browser.find_element_by_xpath('//div[@id="navi01P"]/ul/li[3]').click()

    #【3】株式コードを入力し、検索をクリック
    # 要素が見つかるまで10秒待つ設定
    # browser.implicitly_wait(10) # seconds

    browser.find_element_by_xpath("//input[@id='codeSearch']").send_keys(stock_code)
    browser.find_element_by_name("ACT_clickToSearchStockPriceJP").click()

    #【4】四季報タブをクリック
    # 要素が見つかるまで10秒待つ設定
    # browser.implicitly_wait(10) # seconds

    browser.find_element_by_link_text('四季報').click()

    #【5】財務状況タブをクリック
    # 要素が見つかるまで10秒待つ設定
    # browser.implicitly_wait(10) # seconds

    browser.find_element_by_link_text('財務状況').click()

    #【6】表のデータを取得(テキスト)
    # 要素が見つかるまで10秒待つ設定
    # browser.implicitly_wait(10) # seconds

    elem =browser.find_element_by_xpath("//div[@class= 'shikihouBox01']")

    words = re.split(" +", elem.text)

    return words

def store_words(words):

    #二次元配列rewordsに値を格納
    rewords = []
    buffwords = []
    for word in words:
        if word.__contains__('\n'):
            buff = re.split("\n", word)
            buffwords.append(buff[0])
            #参照渡しだと、clearで一緒に消えてしまうので、copyで値渡しを実施
            rewords.append(buffwords.copy())

            buffwords.clear()
            buffwords.append(buff[1])
        else:
            buffwords.append(word)

    #print('###############')
    #print(rewords)
    #print('###############')

    #もう一度、配列内の体裁を整える(業績の所の列数が合わないので)
    for i in range(len(rewords)):
        #print(rewords[i][0])
        #if rewords[i][0].__contains__("中" or "連" or "四" or "会"):
        if len(rewords[i]) > 7:
            rewords[i][0] += rewords[i][1]
            del rewords[i][1]

    #csvに列方向にそろえるため、空白""を足りない分追加
    for i in range(len(rewords)):
        add_number = 8 - len(rewords[i])
        for _ in range(add_number):
            rewords[i].append("")

    return rewords


####二回目以降のループ

def data_get(stock_code):

    # 要素が見つかるまで10秒待つ設定
    # browser.implicitly_wait(100) # seconds
    browser.find_element_by_xpath("//input[@id='codeSearch']").send_keys(stock_code)
    browser.find_element_by_name("ACT_clickToSearchStockPriceJP").click()

    #【4】四季報タブをクリック
    # 要素が見つかるまで10秒待つ設定
    # browser.implicitly_wait(10000000) # seconds
    # wait = WebDriverWait(browser, 1)
    # wait.until(EC.element_to_be_clickable((By.ID, "四季報")))


    # 要素が見つかるまで10秒待つ設定
    # browser.implicitly_wait(100) # seconds
    # if EC.element_to_be_clickable((By.LINK_TEXT, "財務状況")):
    #     print('true')
    # TODO 株価コードを入力して、対象銘柄が見つからない場合、エラー
    # 【5】財務状況タブをクリック 【6】表のデータを取得(テキスト)
    try:
        browser.find_element_by_link_text('財務状況').click()

        elem =browser.find_element_by_xpath("//div[@class= 'shikihouBox01']")
        words = re.split(" +", elem.text)
        return words
    except NoSuchElementException:
        print('{} 財務データなし'.format(stock_code))
        return ""
    # else:
    #     return ""




if __name__=="__main__":

    stock_codes_file = open('D:/Nan/PycharmProjects/team_development/input_files/sbi_200119/stock_code_200119.csv')
    #stock_codes_file = open('stock_code_highests_180503.csv')
    stock_codes_reader = csv.reader(stock_codes_file)
    stock_codes_data = list(stock_codes_reader)

    print(len(stock_codes_data))

    #グローバル変数の宣言(ネストの中にリストを50個(50行分)を先に追加しておく)
    total_data =[[""] for i in range(50)]

    # try:
    # browser = webdriver.Firefox()
    browser = webdriver.Chrome()

    #[1]ログイン
    login(browser)
    #[2]一つ目のコードのデータ取得
    stock_code = stock_codes_data[1][0]
    words = data_get_initial(stock_code)
    rewords = store_words(words)

    for i in range(len(rewords)):
        for j in range(len(rewords[i])):
            total_data[i].append(rewords[i][j])

    #[3]二つ目以降のコードのデータ取得

#    for i in range(1,len(stock_codes_data)):
    for i in range(0, len(stock_codes_data)):
    # for i in range(0, 10):
        #for i in range(64, len(stock_codes_data)):
        #for i in range(1,10):
        stock_code = stock_codes_data[i][0]
        words = data_get(stock_code)
        rewords = store_words(words)

        for j in range(len(rewords)):
            for k in range(len(rewords[j])):
                total_data[j].append(rewords[j][k])

        #配列の行数を50で統一(足りない分を補完)
        lack_rows = 0
        if len(rewords) < 50:
            lack_rows = 50 - len(rewords)

            for l in range(lack_rows):
                for _ in range(8):
                    total_data[len(rewords) + l].append("")


        print(stock_codes_data[i][0],stock_codes_data[i][1],'{}'.format(i) +' / ' +
              '{} next {} {}'.format(len(stock_codes_data), stock_codes_data[i+1][0],stock_codes_data[i+1][1]))

    # except IndexError as exc:
    #     print('インデックスエラーが起きました{}'.format(exc))
    # except NoSuchElementException:
    #     print('seleniumが要素を見つけられなかった場合のエラーが起きました')
    # except Exception as exc:
    #     print('未知のエラーが起きました{}'.format(exc))


    output_file = open('output_2020.csv','w',newline='')
    output_writer = csv.writer(output_file)
    for i in range(len(total_data)):
        output_writer.writerow(total_data[i])
    output_file.close()

    print('fin')