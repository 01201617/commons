# https://github.com/wanglouis49/pytorch-autoencoders/blob/master/AE.py
# mnistのAE PDのデバイスによって、cuda使用かどうかを分けている(素晴らしい！)
# しかし、(交差)検証はしていないので注意!

import torch
import torchvision.datasets as dsets
import torchvision.transforms as transforms
import torchvision
from torch.autograd import Variable

from time import time

import torch.nn as nn


def get_mnist_data(batch_size):
    """ mnistのdatasetとdata_loaderを取得"""
    dataset = dsets.MNIST(root='../data',
                                train=True,
                                transform=transforms.ToTensor(),
                                download=True)

    # Data loader
    data_loader = torch.utils.data.DataLoader(dataset=dataset,
                                                batch_size=batch_size,
                                                shuffle=True)
    return dataset, data_loader


def to_var(x):
    """ tocrhのライブラリに入力するため、変数型をVariableへ※cudaの有無に対応"""
    if torch.cuda.is_available():
        x = x.cuda()
    return Variable(x)


class Autoencoder(nn.Module):
    """ 3層のAE 入力層(0層)と中間層(1層)のサイズ可変"""
    def __init__(self, in_dim=784, h_dim=400):
        super(Autoencoder, self).__init__()

        self.encoder = nn.Sequential(
            nn.Linear(in_dim, h_dim),
            nn.ReLU()
            )

        self.decoder = nn.Sequential(
            nn.Linear(h_dim, in_dim),
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

    # [0-1] ハイパーパラメーター設定
    num_epochs = 50
    batch_size = 100
    hidden_size = 30
    # [0-2] mnist_data読み込み
    dataset, data_loader = get_mnist_data(batch_size)

    # [1] インスタンス化
    ae = Autoencoder(in_dim=784, h_dim=hidden_size)

    if torch.cuda.is_available():
        ae.cuda()
    # [2] 損失関数、最適化の生成
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(ae.parameters(), lr=0.001)
    iter_per_epoch = len(data_loader)
    data_iter = iter(data_loader)

    # save fixed inputs for debugging
    fixed_x, _ = next(data_iter)
    torchvision.utils.save_image(Variable(fixed_x).data.cpu(), './data/real_images.png')
    fixed_x = to_var(fixed_x.view(fixed_x.size(0), -1))

    # [3] 学習
    for epoch in range(num_epochs):
        t0 = time()
        losses = []
        for i, (images, _) in enumerate(data_loader):

            # flatten the image
            images = to_var(images.view(images.size(0), -1))
            out = ae(images)
            loss = criterion(out, images)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # さらに細かく、学習進度を確認するコード(lossの推移と、特定イメージの再現)
            # losses.append(loss.data)
            # reconst_images_progress = ae(fixed_x)
            # reconst_images_progress = reconst_images_progress.view(reconst_images_progress.size(0), 1, 28, 28)
            # torchvision.utils.save_image(reconst_images_progress.data.cpu(), './data_progress/reconst_images_%d.png' % (i + 1))

            if (i+1) % 100 == 0:
                print ('Epoch [%d/%d], Iter [%d/%d] Loss: %.4f Time: %.2fs'
                    %(epoch+1, num_epochs, i+1, len(dataset)//batch_size, loss.data, time()-t0))

        # save the reconstructed images (AEの生成結果を学習進毎に保存)
        reconst_images = ae(fixed_x)
        reconst_images = reconst_images.view(reconst_images.size(0), 1, 28, 28)
        torchvision.utils.save_image(reconst_images.data.cpu(), './data/reconst_images_%d.png' % (epoch+1))