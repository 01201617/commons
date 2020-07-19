import animatplot as amp
import numpy as np
import matplotlib.pyplot as plt


# 参考URL https://animatplot.readthedocs.io/en/latest/gallery/pcolormesh.html


def function_example(x, y, t):
    """xとyのペアが時間tの時に入力された際の、値を返す(デモンストレーション。数式でなくても良い)

    :param x:
    :param y:
    :param t:
    :return:
    """
    # z = x * y * 100 + t
    z = np.sin(x * x + y * y - t)

    return z


def make_heatmap_gif(X, Y, f, T, colormap='PuBu'):
    """(X, Y)とz=f(x, y, t)となる、関数fとTを入力すれば、それの時間変化のヒートマップを描画する

    :param X: xの一次元のベクトル
    :param Y: yの一次元のベクトル
    :param f: z=f(x, y, t)となる関数f
    :param T: 時間tの一次元のベクトル(時間軸)
    :return: なし


    表記の約束事として、
    x : 要素(値)
    X : 一次元ベクトル
    XX : Xの二次元メッシュ
    XXX : Xの三次元メッシュ
    """
    # TODO (nan) 19/2/21 create,   not complete_method

    XXX, YYY, TTT = np.meshgrid(X, Y, T)

    # 高さ方向(ヒートの値)を関数に従って、時間軸で計算 ※meshはxとyが入れ替わるので注意
    ZZZ = np.zeros((len(Y), len(X), len(T)))

    total = len(Y) * len(X) * len(T)
    count = 0

    for t in T:

        for y in Y:

            for x in X:

                ZZZ[y, x, t] = f(x, y, t)
                count+= 1
                print(count, ' / ', total)

    # ZZZ = np.sin(XXX * XXX + YYY * YYY - TTT)

    # 以下、gif画像描画用コード
    print('描画中')
    block = amp.blocks.Pcolormesh(XXX[:,:,0], YYY[:,:,0], ZZZ, t_axis=2, cmap=colormap)
    plt.colorbar(block.quad)
    # plt.gca().set_aspect('equal')

    anim = amp.Animation([block], amp.Timeline(T))

    anim.controls()

    anim.save_gif('pcolormesh')
    plt.show()
    print('描画完了')


if __name__ == '__main__':
    # (x,y)の座標軸の値(つまり表)が、時間tで変わるとき。

    X = np.arange(0, 20)
    Y = np.arange(0, 100)
    T = np.arange(0, 10)

    make_heatmap_gif(X, Y, function, T, colormap='cool')
