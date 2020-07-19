# -*- coding: utf-8 -*-
import os
import sys

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
    # iDir = os.path.abspath(os.path.dirname(__file__))
    iDir = os.path.abspath(os.path.dirname(sys.argv[0]))

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


def transform_df_to_csv(df, fullpath_output):
    """表データの入ったDataFrameから、データを読み取り、outputフォルダへcsvファイルを出力してくれる(処理時刻付きで)。
    :param df:
    :param fullpath_output:出力ファイルのfullパス
    :return　なし
    """
    # TODO (nan) 19/2/21 create 19/4/11 update


    df.to_csv(fullpath_output, encoding='shift_jis', index=False)
    print('output_csv')