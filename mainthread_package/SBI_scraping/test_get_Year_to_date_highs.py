import csv
import sys
#正規表現用のモジュール
import re
from selenium import webdriver
import os

sys.setrecursionlimit(3000)  # 再帰リミット(リストのリスト、ネストの回数)を1001に設定

#【1】login
def get_tableInfo(browser,stock_code):
    browser.get('https://kabuoji3.com/stock/'+stock_code+'/')

    elem =browser.find_element_by_xpath("//div[@class= 'table_wrap']")
    words = re.split(" +", elem.text)
    return words


def store_words(words):
    """一次元の配列から、日付と終値調整のみをふくんだネストを作成
    """

    #二次元配列rewordsに値を格納
    rewords = []
    buffwords = []
    #最初の要素だけ取得
    buffwords.append(words[0])
    for word in words:
        if word.__contains__('\n'):
            buff = re.split("\n", word)
            buffwords.append(buff[0])
            #参照渡しだと、clearで一緒に消えてしまうので、copyで値渡しを実施
            rewords.append(buffwords.copy())

            buffwords.clear()
            buffwords.append(buff[1])
    return rewords

def store_words_2(words,stock_code,stock_name):
    """一次元の配列から、終値調整のみをふくんだネストを作成
        　さらに、年初来高値か判断(True)→'Highest'を返す
    """
    ishighest = None
    latest_stock = None
    current_stock = None
    hieghst_stock = None
    #現在の株価を取得
    for word in words:
        if word.__contains__('\n'):
            buff = re.split("\n", word)
            #「数字」のみ配列に加える
            if buff[0].isnumeric():
                latest_stock = buff[0]
                current_stock = buff[0]
                hieghst_stock = buff[0]
                break


    #二次元配列rewordsに値を格納
    rewords = []
    rewords.append([stock_code])
    rewords.append([stock_name])
    for word in words:
        if word.__contains__('\n'):
            buff = re.split("\n", word)
            #「数字」のみ配列に加える
            if buff[0].isnumeric():
                current_stock = buff[0]
                rewords.append([current_stock])
                if current_stock > hieghst_stock:
                    hieghst_stock = current_stock

    #最後の数値だけ格納されないので別処理(最後の行は、改行されない==\n含まない)
    current_stock = words[-1]
    rewords.append([current_stock])
    if current_stock > hieghst_stock:
        hieghst_stock = current_stock

    if latest_stock == hieghst_stock:
        ishighest = 'Hieghst'

    return rewords,ishighest,hieghst_stock

def store_words_3(words):
    """一次元の配列から、日付のみをふくんだネストを作成
    """
    #二次元配列rewordsに値を格納
    rewords = []
    #最初の要素だけ取得
    rewords.append(["株式コード"])
    rewords.append(["株式銘柄"])
    rewords.append(["最高値か?"])
    rewords.append(["最高値"])
    rewords.append([words[0]])
    for word in words:
        if word.__contains__('\n'):
            buff = re.split("\n", word)
            #日付の形式の「OO - OO - OO」のみ配列に加える
            if len(buff[1].split('-'))> 1:
                rewords.append([buff[1]])

    # 配列の行数を350で統一(足りない分を補完)
    if len(rewords) < 350:
        lack_rows = 350 - len(rewords)
        current_rows = len(rewords)

        for _ in range(lack_rows):
            rewords.append([""])

    return rewords

def assemble_data(total_table_data,table_data,ishieghst,hiehest_stock):
    """table_dataのリストの結合
    :param table_data:
    :return: total_table_data
    """

    j = 0
    for i in range(len(table_data)):
        if i ==2:
            total_table_data[j].append(ishieghst)
            j += 1
            total_table_data[j].append(hieghst_stock)
            j += 1
            total_table_data[j].append("終値調整")
            j += 1

        total_table_data[j].append(table_data[i][0])
        j  += 1

    # 配列の行数を350で統一(足りない分を補完)
    if len(table_data) < len(total_table_data):
        lack_rows = len(total_table_data) - len(table_data)
        current_rows = len(table_data)

        for l in range(lack_rows-3):
            total_table_data[current_rows + l+3].append("")

    return total_table_data

def get_stock_code(file_name):
    """
    :param url:
    :return: stock_codes_data
    """
    print(os.path.abspath(file_name))
    stock_codes_file = open(file_name)
    stock_codes_reader = csv.reader(stock_codes_file)
    stock_codes_data = list(stock_codes_reader)
    return  stock_codes_data

if __name__=="__main__":
    #[0-1]グローバル変数の宣言とbrowserの立ち上げ(ネストの中にリストを350個(350行分)を先に追加しておく)
    total_table_data =[[""] for i in range(350)]
    browser = webdriver.Chrome()

    #[0-2]対象の株式コード一覧を取得
    # stock_codes_data = get_stock_code('stock_code_180503.csv')
    # stock_codes_data = get_stock_code('stock_code_200102.csv')
    stock_codes_data = get_stock_code('D:/Nan/PycharmProjects/team_development/input_files/sbi_200119/stock_code_200119.csv')
    #stock_codes_data = get_stock_code('stock_code_highests_180503.csv')

    #[0-3]日付だけ先に格納
    buff_data = get_tableInfo(browser,stock_codes_data[0][0])
    total_table_data = store_words_3(buff_data)
    print(total_table_data)

    # [1]main:各銘柄infoをwebから読み取り、該当箇所を抽出し、全体tableへ結合する。
    try:
        for i in range(992, len(stock_codes_data)):
        #for i in range(10):
            # [1-1]各銘柄infoをwebから読み取り
            table_data = get_tableInfo(browser,stock_codes_data[i][0])
            # [1-2] 該当箇所を抽出 & 良い銘柄(上昇トレンドか)かチェック
            re_table_data, ishieghst,hieghst_stock = store_words_2(table_data,stock_codes_data[i][0],stock_codes_data[i][1])
            #print(re_table_data)
            print(stock_codes_data[i][0],stock_codes_data[i][1],'{}'.format(i) +' / ' + '{}'.format(len(stock_codes_data)))

            # [1-3]  全体tableへ結合
            total_table_data = assemble_data(total_table_data,re_table_data,ishieghst,hieghst_stock)
    except Exception as exc:
        print('データ{}取得中に異常発生{}'.format(i, exc))

    # [2] 出力(csv)。
    output_file = open('Year_to_data_highs2_200119.csv','w',newline='')
    output_writer = csv.writer(output_file)
    for i in range(len(total_table_data)):
        output_writer.writerow(total_table_data[i])
    output_file.close()

    print('fin')