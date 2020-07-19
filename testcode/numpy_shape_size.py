import numpy as np


if __name__ =='__main__':
    figs = np.arange(24).reshape(2, 3, 4)

    array_1d_1 = np.array([0, 1])
    array_1d_2 = np.array([2, 3])

    array_2d = np.c_[array_1d_1, array_1d_2, array_1d_1]
    # array_2d = np.concatenate([array_1d_1, array_1d_2, array_1d_1], axis=0)
    array_2d_2 = np.stack([array_1d_1, array_1d_2, array_1d_1], axis=1)
    #
    # print(figs)
    # print((array_1d_1.shape))
    # print(array_2d)
    # print(array_2d_2)