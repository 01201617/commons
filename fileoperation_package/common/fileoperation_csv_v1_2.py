# -*- coding: utf-8 -*-
import os
import sys

import pandas as pd
import tkinter as tk
from tkinter import filedialog as tkFileDialog #python3

import glob


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

def transform_spesific_csv_to_df(csvfile_fullpath):
    """指定フルパスのcsvファイルを読み取り、その中の表データをdfへ格納し、返してくれるメソッド

    :return: DataFrame
    """
    # TODO (nan) 19/4/27 create 19/ update
    # tkアプリウィンドウを表示しないコードです。
    df = pd.read_csv(csvfile_fullpath, header=0, encoding='shift_jis')

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


def transform_csvsinfolder_to_dfs(folder_path):
    """フォルダの中に入った全csvファイルをdfのdictとして変換し返してくれる

    :param folder_path: ~\#
    :return dfs: key:path, value:df
    """
    # TODO (nan) 20/4/25 create

    dfs = {}
    csv_paths = glob.glob(folder_path)
    for csv_path in csv_paths:
        df = pd.read_csv(csv_path, engine="python")
        dfs[csv_path] = df

    return dfs

if __name__ == '__main__':
    dfs = transform_csvsinfolder_to_dfs(r"D:\Nan\PycharmProjects\team_development\input_files\200425__nssac-ncov-data-country-state\*.csv")

    print('fin')