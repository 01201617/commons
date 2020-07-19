import matplotlib.pylab as pyl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def solve_tridiag(a, d, c, b, Ta, Td, Tc, Tb, x, n, Max):
    h = np.zeros((Max), float)
    p = np.zeros((Max), float)

    for i in range(1, n+1):
        a[i] = Ta[i]
        b[i] = Tb[i]
        c[i] = Tc[i]
        d[i] = Td[i]
    h[1] = c[1]/d[1]
    p[1] = b[1]/d[1]

    for i in range(2, n+1):
        h[i] = c[i] / (d[i] - a[i] * h[i-1])
        p[i] = (b[i] - a[i] * p[i-1])/(d[i] - a[i] * h[i-1])
    x[n] = p[n]
    for i in range(n-1, 1, -1):
        x[i] = p[i] - h[i] * x[i+1]

    return x


if __name__ == "__main__":

    # [0] parameter
    Max_t = 1501
    Max_x = 101
    # 空間step数
    n = Max_x-1
    # 時間step数
    m = Max_t-1

    #
    Ta = np.zeros((Max_x), float)
    Tb = np.zeros((Max_x), float)
    Tc = np.zeros((Max_x), float)
    Td = np.zeros((Max_x), float)
    a = np.zeros((Max_x), float)
    b = np.zeros((Max_x), float)
    c = np.zeros((Max_x), float)
    d = np.zeros((Max_x), float)
    # 計算用の変数
    x = np.zeros((Max_x), float)
    # 結果格納用の変数t[x][time]
    t = np.zeros((Max_x, Max_t), float)

    width = 1.0
    h = width / (n-1)

    Dx = 0.03
    Dt = 10
    KAPPA = 210.
    SPH = 900.
    RHO = 2700.
    cons = KAPPA/(SPH*RHO)*Dt/(Dx*Dx)

    # [1] I.C & B.C
    # B.C.
    for i in range(1, m):
        t[0][i] = 0.0
    # I.C.
    for i in range(0, n):
        t[i, 0] = 0.0

    for j in range(1, m+1):
        t[1, j] = 0.0
        t[n, j] = 0.0
    for i in range(2, n):
        t[i][1] = np.sin(np.pi * h * i)
    for i in range(1, n+1):
        Td[i] = 2. + 2./cons
    Td[1] = 1.
    Td[n] = 1.
    # Off diagonal 対角線以外
    for i in range(1, n):
        Ta[i] = -1.0
        Tc[i] = -1.0
    Ta[n-1] = 0.0
    Tc[1] = 0.0
    Tb[1] = 0.0
    Tb[n] = 0.0

    print("I'm working hard, wait for fig while I count to 50")
    # [2] solving
    # 時間step
    for j in range(2, m+1):
        print(j)
        # 現時点でのすべての空間データを更新
        for i in range(2, n):
            Tb[i] = t[i-1][j-1] + t[i+1][j-1] + (2/cons-2) * t[i][j-1]
        x = solve_tridiag(a, d, c, b, Ta, Td, Tc, Tb, x, n, Max_x)
        for i in range(1, n+1):
            t[i][j] = x[i]

    print('finished')
    x = list(range(1, n+1))
    y = list(range(1, m+1))
    X, Y = pyl.meshgrid(x, y)
    Z = t[X, Y]

    fig = pyl.figure()
    ax = Axes3D(fig)
    ax.plot_wireframe(X, Y, Z, color='r')
    ax.set_xlabel('position')
    ax.set_ylabel('time')
    ax.set_zlabel('Temperature')
    pyl.show()





