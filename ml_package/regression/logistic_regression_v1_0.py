import math

import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split

import statsmodels.api as sm


def change_binary(x):
    """0以外を1に、0を0とする関数。dfのapply用に作成

    :param x:
    :return 1 or 0:
    """
    # TODO (nan) 19/4/30 create 19/ update

    if x != 0:
        return 1
    else:
        return 0

def calc_multiple_logistic_regression(x_multi, y_target, data_split=False):
    """多変量のロジスティクス回帰(≒分類 : 目的変数が0と1の二値問題)を実施し、設計変数と精度を返す

    fumula:f(x_multi) = 1/(1+e-t)
           , where t = intercept + b0x0 + b0x0 + …
           参考 : https://qiita.com/0NE_shoT_/items/b702ab482466df6e5569

    :param x: 多次元配列 df型 ※ラベル付き
    :param y: 一次元配列 df(Series)型
    :param datasplit: Trueならデータを訓練用とテスト用に分ける

    :return intercept, coef_df(2次元配列)※変数名付き, score: 設計変数と精度
    """
    # TODO (nan) 19/4/30 create 19/ update

    if data_split:
        # ------------------訓練とテストを分ける場合-------------------------------
        # データをスプリット
        x_train, x_test, y_train, y_test = train_test_split(x_multi, y_target)

        # LogisticRegression()クラスのインスタンス化
        log_model = LogisticRegression()
        # モデル生成
        log_model.fit(x_train, y_train)

        # 訓練データに基づいてsocre取得
        score = log_model.score(x_test, y_test)

    else:
        # ------------------訓練とテストを分けない場合(全てを学習に試用)-------------------------------
        # LogisticRegression()クラスのインスタンス化
        log_model = LogisticRegression()
        # モデル生成
        log_model.fit(x_multi, y_target)

        # 訓練データに基づいてsocre取得
        score = log_model.score(x, y)


    # xの変数名とそれに対応する係数を連結(つまり、bn * xn のbとx)、そして列名を追加
    coef_df = DataFrame([x_multi.columns, log_model.coef_[0]]).T
    coef_df.columns = ['変数名', '係数']

    return log_model.intercept_, coef_df, score

if __name__ == '__main__':
    df = sm.datasets.fair.load_pandas().data
    print(df.head())
    # applyを使って、新しい列用のデータを作成
    df['Had_Affair'] = df['affairs'].apply(change_binary)

    if False:
        # -----------------------------↓データの確認(描画)----------------------------------------------

        print(df.head(10000))

        # groupbyを用いて、Had_Affair列でグループ分けして、各平均を算出
        df_groupby_had_mean = df.groupby('Had_Affair').mean()
        print(df_groupby_had_mean)

        # 不倫の有無で層別して、各項目をヒストグラムで描画
        # 年齢
        sns.countplot('age', data=df, hue='Had_Affair', palette='coolwarm')
        plt.show()

        # 結婚してからの年数
        sns.countplot('yrs_married', data=df, hue='Had_Affair', palette='coolwarm')
        plt.show()

        # 子供の数
        sns.countplot('children', data=df, hue='Had_Affair', palette='coolwarm')
        plt.show()

        # 学歴
        sns.countplot('educ', data=df, hue='Had_Affair', palette='coolwarm')
        plt.show()

    # -----------------------------↓データの前処理----------------------------------------------
    # 質的データを量的データに変換(カテゴリーを表現する変数を、ダミー変数に展開)
    # 詳細:カテゴリ数分、ラベルを作成し、各要素を対応する列に1、それ以外に0を割り振る
    occ_dummies = pd.get_dummies(df['occupation'])
    hus_dummies = pd.get_dummies(df['occupation_husb'])
    # print(occ_dummies.head())

    # 列名を作成し連結
    occ_dummies.columns = ['occ1', 'occ2', 'occ3', 'occ4', 'occ5', 'occ6']
    hus_dummies.columns = ['hocc1', 'hocc2', 'hocc3', 'hocc4', 'hocc5', 'hocc6']
    dummies = pd.concat([occ_dummies, hus_dummies], axis=1)

    # 不要となった、元の列と、目的変数の列を削除し、ダミーデータと連結
    x = df.drop(['occupation', 'occupation_husb', 'Had_Affair'], axis=1)
    x = pd.concat([x, dummies], axis=1)

    # 目的変数の列取得し、dfからnpの一次元の配列としておく
    y = df.Had_Affair
    y = y.values

    # 2列削除で多重共線性を回避。更に、affairs列も削除
    x = x.drop('occ1', axis=1)
    x = x.drop('hocc1', axis=1)
    x = x.drop('affairs', axis=1)
    print(x.head())

    # -----------------------------↓ロジスティクス回帰----------------------------------------------
    intercept, coef_df, score = calc_multiple_logistic_regression(x, y, data_split=True)
    print(coef_df)
    print('fin')

