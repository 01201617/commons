import matplotlib.pylab as pyl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def calc_laplaceline(Nmax=100, Niter=70):
    V = np.zeros((Nmax, Nmax), float)

    print('Working hard, wait for the figure while I count to 60')
    for k in range(0, Nmax -1):
        V[k, 0] = 100

    for iter in range(Niter):
        if iter % 10 == 0:
            print(iter)
        for i in range(1, Nmax - 2):
            for j in range(1, Nmax - 2):
                V[i, j] = 0.25 * (V[i+1, j] + V[i-1, j] + V[i, j+1] + V[i, j-1])
    x = range(0, Nmax-1, 2)
    y = range(0, 50, 2)
    X, Y = pyl.meshgrid(x, y)

    Z = V[X, Y]
    return X, Y, Z


if __name__ == "__main__":
    X, Y, Z = calc_laplaceline(Nmax=100, Niter=70)
    fig = pyl.figure()
    ax = Axes3D(fig)
    ax.plot_wireframe(X, Y, Z, color='r')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Potential')
    pyl.show()

    print('finish')