import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from fileoperation_package.common import fileoperation_csv_v1_0

# 定数項＋ガウス基底(12次元)
def phi(x, s=0.5):
    # sガウス基底の「幅」
    return np.append(1, np.exp(-(x - np.arange(0, 1 + s, s)) ** 2 / (2 * s * s)))


# 正規分布の確率密度関数
def normal_dist_pdf(x, mean, var):
    return np.exp(-(x-mean) ** 2 / (2 * var)) / np.sqrt(2 * np.pi * var)


# 2次形式( x^T A x を計算)
def quad_form(A, x):
    return np.dot(x, np.dot(A, x))


def calc_coditional_probability(x_range, t_range, mu, phi, s, beta, sigma):
    """xとtに対応した条件付き確率 z(x,y) = P(t|x)を計算し、df型の行列z(x,y)を返す

    :param x_range: xの範囲(npの一次元配列)
    :param t_range: yの範囲(npの一次元配列)
    :param mu: 平均μN(mu) (一次元配列)
    :param phi: 基底関数
    :param s: ガウス基底の幅
    :param beta: β 精度
    :param sigma: 共分散行列 (二次元行列)
    :return: df型の行列z(x,y)
    """
    # TODO (nan) 19/3/1 create

    z = np.array([normal_dist_pdf(t_range, np.dot(mu, phi(x, s)),
                                  1 / beta + quad_form(sigma, phi(x, s))) for x in x_range]).T

    # インデックスとcolumns用に、小数点を2桁で固定(後で取得しやすくするため)
    t_range = np.round(t_range, 2)
    x_range = np.round(x_range, 2)
    df_z = pd.DataFrame(data=z, index=t_range, columns=x_range)

    return df_z


def calc_mu_sigma_posterior(PHI, Y, alpha=0.0001, beta=50):
    """    事後分布p(w|t,x) = N(w|μN , ΣN)の平均μN(mu)と共分散行列ΣN(sigma)を計算

    :param PHI:基底関数の線形和（求める関数の候補）
    :param Y:観測値
    :param alpha:
    :param beta:分散の逆数であるこのβは「精度」とも呼ばれています
    :return:mu  = βSNφ(x) T t, sigma = αI  +βφ(x) Tφ(x)
    """
    # TODO (nan) 19/3/1 create

    sigma = np.linalg.inv(alpha * np.identity(PHI.shape[1]) + beta * np.dot(PHI.T, PHI))
    mu = beta * np.dot(sigma, np.dot(PHI.T, Y))

    return mu, sigma

def get_conditional_prob_specific_y(specific_y, x_range, df_z):
    """指定y に対応した条件付き確率 z(x,y)の取り出し

    :param specific_y:
    :param df_z:df_z[x][y]
    :return: conditional_prob(x)
    """
    x_range = np.round(x_range, 2)
    conditional_prob_along_x = np.array([df_z[x][specific_y] for x in x_range])

    return conditional_prob_along_x


def get_conditional_prob_specific_x(specific_x, y_range, df_z):
    """指定y に対応した条件付き確率 z(x,y)の取り出し

    :param specific_x:
    :param df_z:df_z[x][y]
    :return: conditional_prob(y)
    """
    y_range = np.round(y_range, 2)
    conditional_prob_along_y = np.array([df_z[specific_x][y] for y in y_range])

    return conditional_prob_along_y

def main(x_range, y_range, s=0.5, alpha=0.0001, beta=50, specific_x=0.8):
    """    ベイズ線形回帰による事後分布p(w|t,x)を計算し、
    　　　算出された平均μNと共分散行列ΣNに基づき、予測分布を描画する。s,α,βがハイパーパラメータ
        入力の(X, Y)のデータ点は、csvファイルから読み取り(一行目はラベル)※ファイル名とラベル名は英語で！

    :param x_range 例: np.arange(0.4, 1.1, 0.01)
    :param y_range 例: np.arange(0.75, 2.5, 0.01)
    :param s: ガウス基底の幅
    :param alpha:
    :param beta:
    :param specific_x:予測分布の断面の位置を決めるx
    :return:
    """
    # TODO (nan) 19/3/1 create

    df = fileoperation_csv_v1_0.transform_csv_to_df()

    X = df.iloc[1:, 0]
    Y = df.iloc[1:, 1]

    # 事後分布の計算
    PHI = np.array([phi(x, s) for x in X])
    mu, sigma = calc_mu_sigma_posterior(PHI, Y, alpha, beta)

    # ただの線形もグラフ描画しておく
    # w = np.linalg.solve(np.dot(PHI.T, PHI), np.dot(PHI.T, Y))
    # plt.plot(x_range, [np.dot(w, phi(x, s)) for x in x_range], 'g')

    # 近似式の係数
    res_linear = np.polyfit(X, Y, 1)
    Y_hat_linear = np.poly1d(res_linear)(x_range)  # 1次

    #### xとt, それに対応した条件付き確率 z(x,y) = P(t|x)
    df_z = calc_coditional_probability(x_range, y_range, mu, phi, s, beta, sigma)
    z = df_z.values

    ###  描画 ##########################
    plt.plot(x_range, Y_hat_linear, 'g')
    plt.contourf(x_range, y_range, z, 10, cmap=plt.cm.binary)
    plt.plot(x_range, [np.dot(mu, phi(x, s)) for x in x_range], 'r')
    plt.plot(X, Y, 'go')
    plt.xlim(x_range.min(), x_range.max())
    plt.ylim(y_range.min(), y_range.max())
    plt.show()

    ####### 指定x,t に対応した条件付き確率 P(t|x)の取り出し
    y_range = np.round(y_range, 2)
    conditional_prob_along_y = get_conditional_prob_specific_x(specific_x, y_range, df_z)
    plt.plot(y_range, conditional_prob_along_y)
    plt.xlim(y_range.min(), y_range.max())
    plt.show()


###############################　計算実行  ###############################
if __name__ == '__main__':
    x_range = np.arange(0.8, 1.01, 0.01)
    y_range = np.arange(0.6, 1.01, 0.01)

    # 20-15℃
    # main(x_range, y_range, s=0.45, alpha=0.8, beta=10000, specific_x=0.8)

    # 35-15℃
    # main(x_range, y_range, s=0.45, alpha=0.8, beta=10000, specific_x=0.8)

    # 全点
    main(x_range, y_range, s=0.8, alpha=0.8, beta=10000, specific_x=0.8)
