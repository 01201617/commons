import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression


def calc_simple_regression(x, y):
    """単回帰を実施し、設計変数と平均二乗誤差を返す

    :param x: 一次元配列 df(Series)型
    :param y: 一次元配列 df(Series)型
    :return a, b, rmse: 設計変数と平均二乗誤差
    """
    # xを(n, 1)とし、さらに二次元arrayの形に変換(行列の計算形式で実施するため)
    x = np.vstack(x)
    x = np.array([[value, 1] for value in x])
    result = np.linalg.lstsq(x, y, rcond=None)
    a, b = result[0]

    error_total = result[1]
    rmse = np.sqrt(error_total/len(x))

    return a, b, rmse


def calc_multiple_regression(x, y):
    """重回帰を実施し、設計変数と平均二乗誤差を返す

    :param x: 一次元配列 df(Series)型
    :param y: 一次元配列 df(Series)型
    :return intercept, coef(1次元配列), rmse: 設計変数と平均二乗誤差
    """
    # LinearRegression()クラスのインスタンス化
    lreg = LinearRegression()

    #モデル生成
    lreg.fit(x_multi, y_target)

    y_pred = lreg.predict(x)
    error_total = np.sum((y - y_pred) ** 2)
    rmse = np.sqrt(error_total/len(x))

    return lreg.intercept_, lreg.coef_, rmse


if __name__ == '__main__':
    # ----------データ生成--------------
    boston = load_boston()
    # print(boston.DESCR)

    # ----------データ描画(確認)--------------
    plt.hist(boston.target, bins=50)
    plt.xlabel('Price in $1,000s')
    plt.ylabel('Number of houses')
    plt.show()

    plt.scatter(boston.data[:, 5], boston.target)
    plt.xlabel('Number of rooms')
    plt.ylabel('Price in $1,000s')
    plt.show()

    # ----------データ成形(前処理)--------------
    # tupleからdfへ変換 列名つける(元のデータセットを基に)
    boston_df = DataFrame(boston.data)
    boston_df.columns = boston.feature_names

    # 目的変数を新規列に追加
    boston_df['Price'] = boston.target
    print(boston_df.head())

    # ----------単回帰--------------
    # 設計変数と目的変数に一変数ずつ取り出し
    x = boston_df.RM
    y = boston_df.Price
    a, b, rmse = calc_simple_regression(x, y)
    print(a, b, rmse)
    # snsで描画して確認
    sns.lmplot('RM', 'Price', data=boston_df)
    plt.show()

    # ----------重回帰--------------
    # 説明変数(目的変数をテーブルから除く)
    x_multi = boston_df.drop('Price', 1)
    y_target = boston_df.Price
    intercept, coef, rmse = calc_multiple_regression(x_multi, y_target)
    print(intercept, coef, rmse)

