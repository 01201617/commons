import numpy as np
import pandas as pd

from fileoperation_package.common import fileoperation_csv_v1_0
from graph_package.gif import pcolormesh_v0_1


if __name__ == '__main__':
    # TODO (nan) 19/2/22 create

    X = np.arange(0, 20)
    Y = np.arange(0, 100)
    T = np.arange(0, 10)

    f = pcolormesh_v0_1.function_example

    # graph_packageから関数呼び出し使用
    pcolormesh_v0_1.make_heatmap_gif(X, Y, f, T, colormap='cool')

    # 描画した一部の値をfileoperation_packageの関数使ってcsvで保存
    df_X = pd.DataFrame(data=X, columns=['X'])
    df_Y = pd.DataFrame(data=Y, columns=['Y'])
    df_T = pd.DataFrame(data=T, columns=['T'])

    df_all = pd.concat([df_X, df_Y, df_T], axis=1)

    fileoperation_csv_v1_0.transform_df_to_csv(df_all)

    help(pcolormesh_v0_1.make_heatmap_gif)


