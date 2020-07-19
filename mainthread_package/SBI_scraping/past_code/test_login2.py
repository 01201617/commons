import csv
#正規表現用のモジュール
import re

from selenium import webdriver

stock_codes_file = open('stock_code_180503.csv')
stock_codes_reader = csv.reader(stock_codes_file)
stock_codes_data = list(stock_codes_reader)

total_data =[]

#for i in range(5):
stock_code = stock_codes_data[0][0]

####一回目のループだけ特殊

#【1】login
browser = webdriver.Firefox()
browser.get('https://www.sbisec.co.jp/ETGate')

browser.find_element_by_name("user_id").send_keys("305-0285692")
browser.find_element_by_name("user_password").send_keys("KaNT#1617")
browser.find_element_by_name("ACT_login").click()

#【2】国内株式のリンクをクリック
# 要素が見つかるまで10秒待つ設定
browser.implicitly_wait(10) # seconds

browser.find_element_by_xpath('//div[@id="navi01P"]/ul/li[3]').click()

#【3】株式コードを入力し、検索をクリック
# 要素が見つかるまで10秒待つ設定
browser.implicitly_wait(10) # seconds

#browser.find_elements_by_id("codeSearch").send_keys("2003")
#browser.find_element_by_xpath("//input[@id='codeSearch']").send_keys("2003")
#browser.find_element_by_xpath("//input[@id='codeSearch']").send_keys("4004")
browser.find_element_by_xpath("//input[@id='codeSearch']").send_keys(stock_code)
browser.find_element_by_name("ACT_clickToSearchStockPriceJP").click()

#【4】四季報タブをクリック
# 要素が見つかるまで10秒待つ設定
browser.implicitly_wait(10) # seconds

browser.find_element_by_link_text('四季報').click()

#【5】財務状況タブをクリック
# 要素が見つかるまで10秒待つ設定
browser.implicitly_wait(10) # seconds

browser.find_element_by_link_text('財務状況').click()

#【6】表のデータを取得(テキスト)
# 要素が見つかるまで10秒待つ設定
browser.implicitly_wait(10) # seconds

elem =browser.find_element_by_xpath("//div[@class= 'shikihouBox01']")

words = re.split(" +", elem.text)

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

print('###############')
print(rewords)
print('###############')

#もう一度、配列内の体裁を整える(業績の所の列数が合わないので)
for i in range(len(rewords)):
    print(rewords[i][0])
    #if rewords[i][0].__contains__("中" or "連" or "四" or "会"):
    if len(rewords[i]) > 7:
        rewords[i][0] += rewords[i][1]
        del rewords[i][1]

#csvに列方向にそろえるため、空白""を足りない分追加
for i in range(len(rewords)):
    add_number = 8 - len(rewords[i])
    for _ in range(add_number):
        rewords[i].append("")

print(rewords)
total_data = rewords.copy()

####二回目以降のループ

stock_code = stock_codes_data[1][0]

# 要素が見つかるまで10秒待つ設定
browser.implicitly_wait(10) # seconds
browser.find_element_by_xpath("//input[@id='codeSearch']").send_keys(stock_code)
browser.find_element_by_name("ACT_clickToSearchStockPriceJP").click()

#【4】四季報タブをクリック
# 要素が見つかるまで10秒待つ設定
browser.implicitly_wait(10) # seconds

browser.find_element_by_link_text('四季報').click()

#【5】財務状況タブをクリック
# 要素が見つかるまで10秒待つ設定
browser.implicitly_wait(10) # seconds

browser.find_element_by_link_text('財務状況').click()

#【6】表のデータを取得(テキスト)
# 要素が見つかるまで10秒待つ設定
browser.implicitly_wait(10) # seconds

elem =browser.find_element_by_xpath("//div[@class= 'shikihouBox01']")

words = re.split(" +", elem.text)

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

print('###############')
print(rewords)
print('###############')

#もう一度、配列内の体裁を整える(業績の所の列数が合わないので)
for i in range(len(rewords)):
    #if rewords[i][0].__contains__("中" or "連" or "四" or "会"):
     if len(rewords[i]) > 7:
        rewords[i][0] += rewords[i][1]
        del rewords[i][1]

#csvに列方向にそろえるため、空白""を足りない分追加
for i in range(len(rewords)):
    add_number = 8 - len(rewords[i])
    for _ in range(add_number):
        rewords[i].append("")

for i in range(len(rewords)):
    for j in range(len(rewords[i])):
        total_data[i].append(rewords[i][j])

output_file = open('output.csv','w',newline='')
output_writer = csv.writer(output_file)
for i in range(len(total_data)):
    output_writer.writerow(total_data[i])
output_file.close()

print('fin')