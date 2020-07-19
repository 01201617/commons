import matplotlib.pylab as pyl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Todo 未完!!
def calc_analytical_solution(Nmax=100):

    def fourier(x, y, L):
        iter = 21  # フーリエ級数展開の回数
        result = 0
        for n in range(1, iter, 2):
            element = 400/(n * np.pi) * np.sin(n*np.pi*x/L) * np.sinh(n*np.pi*y/L) / np.sinh(n*np.pi)
            result = result + element
        return result

    V = np.zeros((Nmax, Nmax), float)

    print('Working hard, wait for the figure while I count to 60')
    for k in range(0, Nmax - 1):
        V[k, 0] = 100

    for i in range(1, Nmax - 2):
        for j in range(1, Nmax - 2):
            V[i, j] = fourier(i , j, Nmax)

    return X, Y, Z


if __name__ == "__main__":
    X, Y, Z = calc_analytical_solution(Nmax=100)
    fig = pyl.figure()
    ax = Axes3D(fig)
    ax.plot_wireframe(X, Y, Z, color='r')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Potential')
    pyl.show()

    print('finish')