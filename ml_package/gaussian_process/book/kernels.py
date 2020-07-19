import sys
import putil
import numpy as np
from pylab import *
from numpy.random import multivariate_normal as mvnrand

xmax = 5
xmin = -5
ymax = 5
ymin = -5
M = 4
N = 100


def let(val, func):
    return func(val)


def klinear():
    b = randn()
    return lambda x, y: b + x * y


def kexp(sigma):
    return lambda x, y: exp(- abs(x - y) / sigma)


def kgauss(params):
    """[1] ガウスカーネル"関数" ※ を返す
        ※カーネル行列の各要素の計算式
    :param params: [tau, sigma]ハイパーパラメーター
    :return ガウスカーネル(関数):
    """
    [tau, sigma] = params
    return lambda x, y: exp(tau) * exp(-(x - y) ** 2 / exp(sigma))


def kperiodic(params):
    [tau, sigma] = params
    return lambda x, y: exp(tau * cos((x - y) / sigma))


def kmatern3(sigma):
    return lambda x, y: \
        let(abs(x - y), lambda r:
        (1 + sqrt(3) * r / sigma) * exp(- sqrt(3) * r / sigma))


def kmatern5(sigma):
    return lambda x, y: \
        let(abs(x - y), lambda r:
        (1 + sqrt(5) * r / sigma + 5 * r * r / (3 * sigma * sigma))
        * exp(- sqrt(5) * r / sigma))


def kernel_matrix(xx, kernel):
    """[2]カーネル行列を計算し、その行列(np.array※二次元配列)を返す

    :param xx: カーネル行列の大きさを示す行列
    :param kernel: カーネル関数 f(xi, xj)　※カーネル行列の各要素の計算式
    :return　kernel_matrix: カーネル行列(np.array※二次元配列)
    """
    N = len(xx)
    eta = 1e-6
    kernel_matrix = np.array(
        [kernel(xi, xj) for xi in xx for xj in xx]
    ).reshape(N, N) + eta * np.eye(N)
    return kernel_matrix


def fgp(xx, kernel):
    """[3] カーネル行列を用いて、多次元正規分布N(μ,Σ)に従う、ｙの値(1次元ベクトル)を計算する。

    :param xx:
    :param kernel:
    :return:
    """
    N = len(xx)
    K = kernel_matrix(xx, kernel)
    # ライブラリにて、多次元正規分布N(μ,Σ)に従う正規乱数を生成する
    y = mvnrand(np.zeros(N), K)
    return y


def plot_gaussian():
    """[4]描画"""
    xx = np.linspace(xmin, xmax, N)
    for m in range(M):
        plot(xx, fgp(xx, kgauss((1, 1))))



def plot_linear():
    xx = np.linspace(xmin, xmax, N)
    for m in range(M):
        plot(xx, fgp(xx, klinear()))


def plot_exponential():
    xx = np.linspace(xmin, xmax, N)
    for m in range(M):
        plot(xx, fgp(xx, kexp(1)))


def plot_periodic():
    xx = np.linspace(xmin, xmax, N)
    for m in range(M):
        plot(xx, fgp(xx, kperiodic((1, 0.5))))


def plot_matern3():
    xx = np.linspace(xmin, xmax, N)
    for m in range(M):
        plot(xx, fgp(xx, kmatern3(1)))


def plot_matern5():
    xx = np.linspace(xmin, xmax, N)
    for m in range(M):
        plot(xx, fgp(xx, kmatern5(1)))


def usage():
    print('usage: kernels.py kernel [output]')
    sys.exit(0)


def main(name='gaussian'):
    # args(引数)による指定を、コード内での指定に変更!
    # if len(sys.argv) < 2:
    #     usage()
    # else:
    #     name = sys.argv[1].lower()

    if name == 'gaussian':
        plot_gaussian()
    elif name == 'linear':
        plot_linear()
    elif name == 'periodic':
        plot_periodic()
    elif name == 'exponential':
        plot_exponential()
    elif name == 'matern3':
        plot_matern3()
    elif name == 'matern5':
        plot_matern5()
    else:
        print('unknown kernel.')
        usage()

    # ↓エラー出るので、とりあえず、コメントアウト
    # putil.simpleaxis()
    # axis([xmin, xmax, ymin, ymax])
    #
    # if len(sys.argv) > 2:
    #     putil.savefig(sys.argv[2])
    show()


if __name__ == "__main__":
    main(name='gaussian')