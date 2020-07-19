#    gpr.py -- Gaussian process regression.
#    $Id: gpr.py,v 1.3 2017/11/12 04:51:52 daichi Exp $
#
import sys
import putil
import numpy as np
# from pylab import *
from numpy import exp, sqrt
from numpy.linalg import inv
from preprocess_package import covid19
import matplotlib.pyplot as plt



# GP kernel parameters
eta = 0.05 #　大きくなると、(全体の)範囲拡大
tau = 1000 #　大きくなると、(特に外挿の)範囲拡大
sigma = 100 #　大きくなると、直線性up


def kgauss(params):
    [tau, sigma] = params
    return lambda x, y: tau * exp(-(x - y) ** 2 / (2 * sigma * sigma))


def kv(x, xtrain, kernel):
    return np.array([kernel(x, xi) for xi in xtrain])


def kernel_matrix(xx, kernel):
    """[1] カーネル行列を計算　※詳しくは、kernels.pyプログラムを参照"""
    N = len(xx)
    return np.array(
        [kernel(xi, xj) for xi in xx for xj in xx]
    ).reshape(N, N) + eta * np.eye(N)


def gpr(xx, xtrain, ytrain, kernel):
    """[2]ガウス過程の予測分布計算し、 y予測値の生成用※の、平均値,分散を返す
    ※ y ~ 多次元正規分布N(平均値,分散)
         ypr(平均) = kT ・ K-1 ・ ytrain
         spr(分散) = - kT ・ K-1 ・ k

    :param xx:
    :param xtrain:
    :param ytrain:
    :param kernel:
    :return:
    """
    # カーネル行列を取得
    K = kernel_matrix(xtrain, kernel)
    Kinv = inv(K)
    ypr = []
    spr = []
    for x in xx:
        s = kernel(x, x) + eta
        k = kv(x, xtrain, kernel)
        # ypr(平均) = kT ・ K-1 ・ ytrain
        ypr.append(k.T.dot(Kinv).dot(ytrain))
        # spr(分散) = - kT ・ K-1 ・ k
        spr.append(s - k.T.dot(Kinv).dot(k))
    return ypr, spr


def gpplot(xx, xtrain, ytrain, kernel, params):
    """[3] 予測分布(ガウス分布)の平均値、分散の値より、yの予測分布を計算し、描画する

    :param xx: 計算したいxの 1次元ベクトル
    :param xtrain:
    :param ytrain:
    :param kernel: 計算に用いるカーネル関数
    :param params:
    :return:
    """
    # ガウス過程の予測分布計算し、各計算したいxに対するyの平均値と分散を取得
    ypr, spr = gpr(xx, xtrain, ytrain, kernel(params))
    # 学習データ(実測値)と予測平均値を描画 (それぞれ、プロットと実践により)
    plt.plot(xtrain, ytrain, 'bx', markersize=16)
    plt.plot(xx, ypr, 'b-')

    # 予測分布の領域(事後分布±2σ)を描画
    yymin = ypr - 2 * sqrt(spr)
    yymax = ypr + 2 * sqrt(spr)
    plt.fill_between(xx, yymin, yymax, color='#ccccff')


def usage():
    print('usage: gpr.py train output')
    print('$Id: gpr.py,v 1.3 2017/11/12 04:51:52 daichi Exp $')
    sys.exit(0)


def main(df_input):




    xtrain = df_input.iloc[:, 0].values
    xtrain = xtrain.astype(float)
    ytrain = df_input.iloc[:, 1].values
    ytrain = ytrain.astype(float)
    ytrain = np.log10(ytrain)

    kernel = kgauss
    params = [tau, sigma]

    # plot parameters
    N = 1000
    xmin = 0
    xmax = max(xtrain)*3

    xx = np.linspace(xmin, xmax, N)

    # 予測分布の計算と描画
    gpplot(xx, xtrain, ytrain, kernel, params)

    # ↓エラー出るので、とりあえず、コメントアウト
    # putil.simpleaxis()
    # if len(sys.argv) > 2:
    #     savefig(sys.argv[2])
    # else:
    #     show()
    plt.xlabel('cumurative_day_from20/1/22[days]')
    plt.ylabel('Number of infected people[10^n]')
    plt.xlim(0, 150)
    plt.ylim(0, 6)
    plt.show()


if __name__ == "__main__":
    df_infos = covid19.get_infos(country='Japan')
    main(df_infos.loc[:,['cum_days[day]', 'confirmed[person]']])