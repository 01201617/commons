#    gpr.py -- Gaussian process regression.
#    $Id: gpr.py,v 1.14 2018/03/09 00:55:08 daichi Exp $
#
#
import sys
import putil
import numpy as np
from pylab import *
from numpy.linalg import det, inv
from scipy.optimize import minimize, fmin_l_bfgs_b
# from scg import SCG
from pyGPs.Optimization import scg
from preprocess_package import covid19




def kgauss(params):
    [tau, sigma, eta] = params
    return lambda x, y, train=True: \
        exp(tau) * exp(-(x - y) ** 2 / exp(sigma)) + \
        (exp(eta) if (train and x == y) else 0)


def kgauss_grad(xi, xj, d, kernel, params):
    """[1] カーネル関数k(xi, xj|θ)の微分した'関数'(つまり導関数)を返す※

     ※ハイパラθが3変数あるため、微分も3通りある。
        1. tau
        2. sigma
        3. eta
     """
    # tauで微分した場合
    if d == 0:
        return exp(params[d]) * kernel(params)(xi, xj)
    # sigmaで微分した場合
    if d == 1:
        return kernel(params)(xi, xj) * \
               (xi - xj) * (xi - xj) / exp(params[d])
    # etaで微分した場合
    if d == 2:
        return (exp(params[d]) if xi == xj else 0)
    else:
        return 0


def kv(x, xtrain, kernel):
    return np.array([kernel(x, xi, False) for xi in xtrain])


def kernel_matrix(xx, kernel):
    N = len(xx)
    return np.array(
        [kernel(xi, xj) for xi in xx for xj in xx]
    ).reshape(N, N)


def gpr(xx, xtrain, ytrain, kernel):
    K = kernel_matrix(xtrain, kernel)
    Kinv = inv(K)
    ypr = [];
    spr = []
    for x in xx:
        s = kernel(x, x)
        k = kv(x, xtrain, kernel)
        ypr.append(k.T.dot(Kinv).dot(ytrain))
        spr.append(s - k.T.dot(Kinv).dot(k))
    return ypr, spr


def tr(A, B):
    return (A * B.T).sum()


def printparam(params):
    print(params)


def loglik(params, xtrain, ytrain, kernel, kgrad):
    """[2-1 最適化準備(目的関数L)] 最小化すべき、L = log p(y|X,θ) = -log|K|-yT ・ K-1 ・ yの関数(今回の目的関数)を返す"""
    K = kernel_matrix(xtrain, kernel(params))
    Kinv = inv(K)
    return log(det(K)) + ytrain.T.dot(Kinv).dot(ytrain)
    # return (N * log(2*np.pi) + \
    #         log(det(K)) + ytrain.T.dot(Kinv).dot(ytrain)) / 2


def gradient(params, xtrain, ytrain, kernel, kgrad):
    """[2-2 目的関数の導関数]傾きdL/dθ※の要素が入ったベクトル[dL/tau, dl/sigma, dl/eta]を返す
    ※  dL/dθ = -tr(K-1 dK/dθ) + (K-1 y)T ・ dK/dθ ・ (K-1 y)
    """
    K = kernel_matrix(xtrain, kernel(params))
    Kinv = inv(K)
    Kinvy = Kinv.dot(ytrain)
    D = len(params)
    N = len(xtrain)
    grad = np.zeros(D)
    for d in range(D):
        G = np.array(
            [kgrad(xi, xj, d, kernel, params)
             for xi in xtrain for xj in xtrain]
        ).reshape(N, N)
        # dL/dθ = -tr(K-1 dK/dθ) + (K-1 y)T ・ dK/dθ ・ (K-1 y)
        grad[d] = tr(Kinv, G) - Kinvy.dot(G).dot(Kinvy)
    return grad


def numgrad(params, xtrain, ytrain, kernel, kgrad, eps=1e-6):
    """[2-2' 目的関数の導関数]傾きdL/dθ※の要素が入ったベクトル[dL/tau, dl/sigma, dl/eta]を返す
    ※  ここでは数値的に算出している
        dL/dθ　= (newlik - lik) / eps
    """
    D = len(params)
    ngrad = np.zeros(D)
    for d in range(D):
        lik = loglik(params, xtrain, ytrain, kernel, kgrad)
        params[d] += eps
        newlik = loglik(params, xtrain, ytrain, kernel, kgrad)
        params[d] -= eps
        ngrad[d] = (newlik - lik) / eps
    return ngrad


def optimize(xtrain, ytrain, kernel, kgrad, init):
    """[3 最適化] sk-learnのminimize関数を用いて、パラメーターを最適化し、その値を返す
        ※sk-learnのfmin_l_bfgs_b関数でも同様にできる　＠ optimize2
    """

    # sk-learnのminimize関数で最適化。以下、引数の説明
    # loglik : 今回の目的関数 f(xtrain, ytrain, kernel, kgrad)
    # args : 目的関数に入力する引数
    # jac : ヤコビアン行列 :傾きdL/dθ※の要素が入った行列を ※ dL/dθ = -tr(K-1 dK/dθ) + (K-1 y)T ・ dK/dθ ・ (K-1 y)
    res = minimize(loglik, init, args=(xtrain, ytrain, kernel, kgrad),
                   jac=gradient,  # numgrad
                   method='BFGS', callback=printparam,
                   options={'gtol': 1e-4, 'disp': True})
    print(res.message)
    return res.x


def optimize1(xtrain, ytrain, kernel, kgrad, init):
    # TODO うまく、scgが動作できない
    x, flog, feval, status = scg(loglik, gradient, init,
                                 optargs=[xtrain, ytrain, kernel, kgrad])
    print(status)
    return x


def optimize2(xtrain, ytrain, kernel, kgrad, init):
    """[3 最適化]  sk-learnのfmin_l_bfgs_b関数を用いて、パラメーターを最適化し、その値を返す
    """
    # sk-learnのminimize関数で最適化。以下、引数の説明
    # loglik : 今回の目的関数 f(xtrain, ytrain, kernel, kgrad)
    # args : 目的関数に入力する引数
    # fprime : ヤコビアン行列 :傾きdL/dθ※の要素が入った行列を ※ dL/dθ = -tr(K-1 dK/dθ) + (K-1 y)T ・ dK/dθ ・ (K-1 y)

    x, f, d = fmin_l_bfgs_b(loglik, init, fprime=gradient,
                            args=[xtrain, ytrain, kernel, kgrad],
                            iprint=0, maxiter=1000)
    print(d)
    return x


def gpplot(xtrain, ytrain, kernel, params, xmin=0, xmax=100, N=100, color='#ccccff'):
    xx = np.linspace(xmin, xmax, N)
    ypr, spr = gpr(xx, xtrain, ytrain, kernel(params))
    plot(xtrain, ytrain, 'bx', markersize=16)
    # plot(xx, ypr, 'b-')
    fill_between(xx, ypr - 2 * sqrt(spr), ypr + 2 * sqrt(spr), color=color)


def usage():
    print('usage: gpr.py train [output]')
    print('$Id: gpr.py,v 1.14 2018/03/09 00:55:08 daichi Exp $')
    sys.exit(0)


def main(df_input):
    # # args(引数)による指定を、コード内での指定に変更!
    # if len(sys.argv) < 2:
    #     usage()
    # else:
    #     train = np.loadtxt(sys.argv[1], dtype=float)


    # kernel parameters
    tau = log(1)
    sigma = log(1)
    eta = log(1)


    xtrain = df_input.iloc[:, 0].values
    xtrain = xtrain.astype(float)
    xtrain = xtrain / (max(xtrain) - min(xtrain))

    ytrain = df_input.iloc[:, 1].values
    ytrain = ytrain.astype(float)
    ytrain = np.log10(ytrain)
    # ytrain = (ytrain - mean(ytrain))/std(ytrain)

    # カーネル行列とカーネル行列の導関数(微分後)を取得
    kernel = kgauss
    kgrad = kgauss_grad
    params = np.array([tau, sigma, eta])

    print('params_init. =')
    print(params)

    # 計算に用いる、傾きdL/dθをプリント :gradient(解析的)、numgrad(数値的)
    print('ngrad =', numgrad(params, xtrain, ytrain, kernel, kgrad))
    print('grad  =', gradient(params, xtrain, ytrain, kernel, kgrad))

    # ハイパラθ(tau, sigma, eta)の最適化 : 学習データ、目的関数(log p(y|X,θ))、目的関数の引数、設計変数、導関数dL/dθ
    params = optimize2(xtrain, ytrain, kernel, kgrad, params)
    # params = optimize2(xtrain, ytrain, kernel, kgrad, params)

    # 算出したハイパラと、そこから求める予測分布の出力
    print('params =')
    print(params)

    # plot parameters
    N = 1000
    xmin = 0
    xmax = max(xtrain)*10

    gpplot(xtrain, ytrain, kernel, params, xmin=xmin, xmax=xmax, N=N)

    # ↓エラー出るので、とりあえず、コメントアウト
    # putil.simpleaxis()
    #
    # if len(sys.argv) > 2:
    #     savefig(sys.argv[2])
    show()


if __name__ == "__main__":
    df_infos = covid19.get_infos(country='Japan')
    main(df_infos.loc[:,['cum_days[day]', 'confirmed[person]']])