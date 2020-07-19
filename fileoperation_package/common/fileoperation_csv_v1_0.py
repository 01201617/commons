# -*- coding: utf-8 -*-
import datetime
import os

import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import filedialog as tkFileDialog #python3


def transform_csv_to_df():
    """ポップアップから(複数の)csvファイルを読み取り、その中の表データをdfへ格納し、返してくれるメソッド

    :return: DataFrame
    """
    # TODO (nan) 19/2/21 create 19/2/22 update
    # tkアプリウィンドウを表示しないコードです。
    root = tk.Tk()
    root.withdraw()

    fTyp = [("", "*.csv")]
    iDir = os.path.abspath(os.path.dirname(__file__))

    # askopenfilename 複数のファイルを選択する。
    filenames = tkFileDialog.askopenfilenames(filetypes=fTyp, initialdir=iDir)

    dfs = []

    for filename in filenames:
        df = pd.read_csv(filename, header=0, encoding='shift_jis')
        dfs.append(df)

    i = 0
    for df in dfs:
        print(dfs[i])
        i = i + 1

    return df


def transform_df_to_csv(df):
    """表データの入ったDataFrameから、データを読み取り、outputフォルダへcsvファイルを出力してくれる(処理時刻付きで)。
    :param df:
    :return　なし
    """
    # TODO (nan) 19/2/21 create 19/2/22 update

    if not os.path.isdir('output'):
        os.mkdir('output')

    now = datetime.datetime.now()
    curr_time = 'test_{0:%Y%m%d%H%M}'.format(now)
    df.to_csv("output/output_{}.csv".format(curr_time),
              encoding='shift_jis', index=False)
    print('output_csv')