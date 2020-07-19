import matplotlib.pylab as pyl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np



if __name__ == "__main__":

    # [0] parameter
    Nx = 101
    Nt = 30000
    #  結果格納用時間刻み幅
    step_t = Nt/100
    Dx = 0.03
    Dt = 1.0
    KAPPA = 210.
    SPH = 900.
    RHO = 2700.
    # 計算用T配列※時間は、現在のステップと1ステップ前のみ
    T = np.zeros((Nx, 2), float)
    # 結果格納用T配列
    Tpl = np.zeros((Nx, int(Nt/step_t +1)), float)

    print('Working, wait for figure after count to 10')

    # [1] I.C & B.C
    for ix in range(1, Nx-1):
        T[ix, 0] = 100.0

    T[0, 0] = 0.0
    T[0, 1] = 0.
    T[Nx-1] = 0.
    T[Nx-1, 1] = 0.0
    cons = KAPPA/(SPH*RHO)*Dt/(Dx*Dx)
    m = 1

    # [2] solving
    for t in range(1, Nt):
        # 時間発展計算(陽解放、前進差分)
        for ix in range(1, Nx-1):
            T[ix, 1] = T[ix, 0] + cons * (T[ix+1, 0] + T[ix-1, 0] - 2.*T[ix, 0])
        # 結果格納用
        if t % step_t == 0 or t == 1:
            for ix in range(1, Nx-1, 2):
                Tpl[ix, m] = T[ix, 1]
            print(m)
            m = m + 1
        # 時間更新(1step前の時間を設定)
        for ix in range(1, Nx-1):
            T[ix, 0] = T[ix, 1]
    x = list(range(1, Nx-1, 2))
    y = list(range(1, int(Nt/step_t)))
    X, Y = pyl.meshgrid(x, y)
    Z = Tpl[X, Y]

    fig = pyl.figure()
    ax = Axes3D(fig)
    ax.plot_wireframe(X, Y, Z, color='r')
    ax.set_xlabel('position')
    ax.set_ylabel('time')
    ax.set_zlabel('Temperature')
    pyl.show()