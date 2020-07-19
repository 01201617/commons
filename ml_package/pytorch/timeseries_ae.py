# https://techblog.istyle.co.jp/archives/4318

import numpy as np
import matplotlib.pyplot as plt
import torch
from torch.autograd import Variable
from time import time
import torch.nn as nn


def to_var(x):
    """ tocrhのライブラリに入力するため、変数型をVariableへ※cudaの有無に対応"""
    if torch.cuda.is_available():
        x = x.cuda()
    return Variable(x)


def create_timeseries_data(input_data_length, nomal_size, anomal_size_1, anomal_size_2):
    # データ長100のsin波にノイズ大を足したデータを10000個作成 (正常 10000)
    big_noise_sin = np.array([np.sin( np.linspace(0, np.pi*2, input_data_length) )
                              + np.random.randn(input_data_length) * 0.5 for _ in range(nomal_size) ])

    # データ長100のsin波にノイズ小を足したデータを100個作成　(異常小 100)
    small_noise_sin = np.array([np.sin( np.linspace(0, np.pi*2, input_data_length) )
                                + np.random.randn(input_data_length) * 0.1 for _ in range(anomal_size_1) ])

    # データ長100のcos波にノイズ小を足したデータを100個作成　(異常大 100)
    smallnoise_bigwave_cos = np.array([np.cos( np.linspace(0, np.pi*2, input_data_length) ) * 2
                                + np.random.randn(input_data_length) * 0.5 for _ in range(anomal_size_2) ])

    return big_noise_sin, small_noise_sin, smallnoise_bigwave_cos


def visualize(array):
    plt.figure(figsize=(12, 8))
    _ = [ plt.plot(np.arange(0, input_data_length), x) for x in array]
    plt.ylim(0, 1)
    plt.show()

class Autoencoder(nn.Module):
    """ 3層のAE 入力層(0層)と中間層(1層)のサイズ可変"""
    def __init__(self, in_dim=784, h_dim1=30, h_dim2=10):
        super(Autoencoder, self).__init__()

        self.encoder = nn.Sequential(
            nn.Linear(in_dim, h_dim1),
            nn.ReLU(),
            nn.Linear(h_dim1, h_dim2),
            nn.ReLU()
            )

        self.decoder = nn.Sequential(
            nn.Linear(h_dim2, h_dim1),
            nn.Linear(h_dim1, in_dim),
            nn.Sigmoid()
            )


    def forward(self, x):
        """
        Note: image dimension conversion will be handled by external methods
        """
        out = self.encoder(x)
        out = self.decoder(out)
        return out

if __name__ == '__main__':

    # [0 学習データ生成]
    # 時系列データ長を100とする
    input_data_length = 100
    big_noise_sin, small_noise_sin, smallnoise_bigwave_cos = create_timeseries_data(input_data_length, 10000, 100, 100)
    # データ結合
    input_data = np.vstack([small_noise_sin, big_noise_sin, smallnoise_bigwave_cos])
    # データをシャッフル
    # np.random.seed(seed=42)
    np.random.shuffle(input_data)

    # 正規化 max=1, min=0に
    min = np.min(input_data)
    max = np.max(input_data)
    input_data = (input_data - min) / (max - min)

    print('visualization')
    # 全時系列データを可視化
    # visualize(big_noise_sin[0:100, :])
    # visualize(small_noise_sin)
    # visualize(smallnoise_bigwave_cos)

    #ハイパーパラメーター設定
    num_epochs = 1000
    batch_size = 100
    hidden_size_1 = 70
    hidden_size_2 = 30

    # [1] インスタンス化
    ae = Autoencoder(in_dim=input_data_length, h_dim1=hidden_size_1, h_dim2=hidden_size_2)
    if torch.cuda.is_available():
        ae.cuda()

    # [2] 損失関数、最適化の生成
    criterion = nn.BCELoss()
    # criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(ae.parameters(), lr=0.0001)

    # [3] 学習
    for epoch in range(num_epochs):
        t0 = time()
        losses = []
        itr_num = int(len(input_data)/batch_size)
        inputs_shffle = input_data.copy()
        np.random.shuffle(inputs_shffle)
        for i in range(itr_num):


            # flatten the inputs
            inputs_np = inputs_shffle[i * batch_size:(i + 1) * batch_size, :]
            inputs_torch = torch.from_numpy(inputs_np)
            inputs = to_var(inputs_torch).float()

            out = ae(inputs)
            loss = criterion(out, inputs)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # さらに細かく、学習進度を確認するコード(lossの推移と、特定イメージの再現)
            losses.append(loss.data)

            if (i+1) % itr_num == 0:
                print ('Epoch [%d/%d], Iter [%d/%d] Loss: %.4f Time: %.2fs'
                    %(epoch+1, num_epochs, i+1, len(input_data)//batch_size, loss.data, time()-t0))

        if (epoch+1) % 100 == 0:
            test = smallnoise_bigwave_cos[0:10, :]
            test = (test - min) / (max - min)
            visualize(test)

            inputs_torch = torch.from_numpy(test)
            inputs = to_var(inputs_torch).float()
            out = ae(inputs)
            visualize(out.data.cpu())

    print('fin')