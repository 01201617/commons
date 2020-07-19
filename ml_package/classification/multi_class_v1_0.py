import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

sns.set_style('whitegrid')

def change_to_flower_name(num):
    """対応する0-2の数字を、花名に変換(dfのapply用)

    :param num:
    :returns 花名('Setosa' 'Veriscolour' 'Virginica')
    """
    # TODO (nan) 19/4/30 create 19/ update

    if num == 0:
        return 'Setosa'
    elif num == 1:
        return 'Veriscolour'
    else:
        return 'Virginica'


def calc_multiple_logistic_classification(x_multi, y_target, data_split=True):
    """多変量のロジスティクス回帰での分類を実施し、設計変数と精度を返す

    :param x: 多次元配列 df型 ※ラベル付き
    :param y: 一次元配列 df(Series)型
    :param datasplit: Trueならデータを訓練用とテスト用に分ける

    :return intercept, coef_df(2次元配列)※変数名付き_0列目の値のみ！, score: 設計変数と精度
    """
    # TODO (nan) 19/4/30 create 19/ update

    if data_split:
        # ------------------訓練とテストを分ける場合-------------------------------
        # データをスプリット(一応、テストの比率を40%として、randomのseedも固定している)
        x_train, x_test, y_train, y_test = train_test_split(x_multi, y_target, test_size=0.4, random_state=3)

        # LogisticRegression()クラスのインスタンス化
        log_model = LogisticRegression()
        # モデル生成
        log_model.fit(x_train, y_train)

        # 訓練データに基づいてsocre取得
        score = log_model.score(x_test, y_test)

    else:
        # ------------------訓練とテストを分けない場合(全てを学習に試用)-------------------------------
        # LogisticRegression()クラスのインスタンス化
        log_model = LogisticRegression()
        # モデル生成
        log_model.fit(x_multi, y_target)

        # 訓練データに基づいてsocre取得
        score = log_model.score(x, y)


    # xの変数名とそれに対応する係数を連結(つまり、bn * xn のbとx)、そして列名を追加
    coef_df = DataFrame([x_multi.columns, log_model.coef_[0]]).T
    coef_df.columns = ['変数名', '係数']

    return log_model.intercept_, coef_df, score


def calc_knn(x_multi, y_target, data_split=True, n_neighbors=6):
    """k近傍法(k-nearest neighbor)での分類を実施し、学習済みモデルと精度を返す

    :param x: 多次元配列 df型 ※ラベル付き
    :param y: 一次元配列 df(Series)型
    :param datasplit: Trueならデータを訓練用とテスト用に分ける

    :return knn(モデルを返す!)※sklearnインポートしておく必要あり, score: 設計変数と精度
    """
    # TODO (nan) 19/4/30 create 19/ update

    if data_split:
        # ------------------訓練とテストを分ける場合-------------------------------
        # データをスプリット(一応、テストの比率を40%として、randomのseedも固定している)
        x_train, x_test, y_train, y_test = train_test_split(x_multi, y_target, test_size=0.4, random_state=3)
        # k=6からはじめてみます。
        # インスタンスを作ります。
        knn = KNeighborsClassifier(n_neighbors=n_neighbors)

        # 学習します。
        knn.fit(x_train, y_train)

        # テストデータを予測します。
        y_pred = knn.predict(x_test)

        # 訓練データに基づいてsocre取得
        score = knn.score(x_test, y_test)

    else:
        # k=6からはじめてみます。
        # インスタンスを作ります。
        knn = KNeighborsClassifier(n_neighbors=n_neighbors)

        # 学習します。
        knn.fit(x_multi, y_target)

        # 訓練データに基づいてsocre取得
        score = knn.score(x_multi, y_target)


    return knn, score


def calc_svm(x_multi, y_target, data_split=True, kernel='rbf'):
    """サポートベクターマシン(SVM)での分類を実施し、学習済みモデルと精度を返す

    :param x: 多次元配列 df型 ※ラベル付き
    :param y: 一次元配列 df(Series)型
    :param datasplit: Trueならデータを訓練用とテスト用に分ける

    :param kernel: svmのパラメーター(linear, rbf, poly)

    :return svm_model(モデルを返す!)※sklearnインポートしておく必要あり, score: 設計変数と精度
    """
    # TODO (nan) 19/4/30 create 19/ update

    if data_split:
        # ------------------訓練とテストを分ける場合-------------------------------
        # データをスプリット(一応、テストの比率を40%として、randomのseedも固定している)
        x_train, x_test, y_train, y_test = train_test_split(x_multi, y_target, test_size=0.4, random_state=3)
        # k=6からはじめてみます。
        # インスタンスを作ります。
        svm_model = SVC(kernel=kernel)

        # 学習します。
        svm_model.fit(x_train, y_train)

        # テストデータを予測します。
        y_pred = svm_model.predict(x_test)

        # 訓練データに基づいてsocre取得
        score = svm_model.score(x_test, y_test)

    else:
        # k=6からはじめてみます。
        # インスタンスを作ります。
        svm_model = SVC(kernel=kernel)

        # 学習します。
        svm_model.fit(x_multi, y_target)

        # 訓練データに基づいてsocre取得
        score = svm_model.score(x_multi, y_target)


    return svm_model, score


def calc_gaussian_naive_bayes(x_multi, y_target, data_split=True):
    """サポートベクターマシン(SVM)での分類を実施し、学習済みモデルと精度を返す

    :param x: 多次元配列 df型 ※ラベル付き
    :param y: 一次元配列 df(Series)型
    :param datasplit: Trueならデータを訓練用とテスト用に分ける

    :return svm_model(モデルを返す!)※sklearnインポートしておく必要あり, score: 設計変数と精度
    """
    # TODO (nan) 19/4/30 create 19/ update

    if data_split:
        # ------------------訓練とテストを分ける場合-------------------------------
        # データをスプリット(一応、テストの比率を40%として、randomのseedも固定している)
        x_train, x_test, y_train, y_test = train_test_split(x_multi, y_target, test_size=0.4, random_state=0)
        # k=6からはじめてみます。
        # インスタンスを作ります。
        bayes_model = GaussianNB()

        # 学習します。
        bayes_model.fit(x_train, y_train)

        # テストデータを予測します。
        y_pred = bayes_model.predict(x_test)

        # 訓練データに基づいてsocre取得
        score = bayes_model.score(x_test, y_test)

    else:
        # k=6からはじめてみます。
        # インスタンスを作ります。
        bayes_model = GaussianNB()

        # 学習します。
        bayes_model.fit(x_multi, y_target)

        # 訓練データに基づいてsocre取得
        score = bayes_model.score(x_multi, y_target)


    return bayes_model, score


def make_2Dgraph_predicted_result(model, x_2varables, y):
    """学習済みmodelから求まった境界線を、引数の2変数2次元図へプロット

    :param model:
    :param x_2varables:
    :param y:
    :return:
    """
    # step_size
    h = 0.02

    # 横軸(horizontal)の最大最小
    h_min=x[:, 0].min() - 1
    h_max=x[:, 0].max() + 1

    # 縦軸(vertical)の最大最小
    v_min = x[:, 1].min() - 1
    v_max = x[:, 1].max() + 1

    # meshgridを作る
    hh, vv = np.meshgrid(np.arange(h_min, h_max, h), np.arange(v_min, v_max, h))

    # 境界線を描画
    plt.figure(figsize=(15, 15))
    z = model.predict(np.c_[hh.ravel(), vv.ravel()])

    z = z.reshape(hh.shape)

    plt.contourf(hh, vv, z, cmap=plt.cm.terrain, alpha=0.5, linewidths=0)

    plt.scatter(x_2varables.iloc[:, 0], x_2varables.iloc[:, 1], c=y, cmap=plt.cm.Dark2)

    plt.xlim(hh.min(), hh.max())
    plt.ylim(vv.min(), vv.max())
    plt.xticks(())
    plt.yticks(())
    plt.show()


if __name__ == '__main__':

    """アヤメ分類問題
    
    4つの説明変数
        sepal_length (cm)
        sepal_width (cm)
        petal_length (cm)
        petal_width (cm)
    
    3つのクラス
        Iris-setosa (n=50)
        Iris-versicolor (n=50)
        Iris-virginica (n=50)    
    
    詳しくは⇒ print(iris.DESCR)
    
    """
    iris = load_iris()
    x = iris.data
    y = iris.target

    # -----------------------------↓データの前処理----------------------------------------------
    # DataFrameとして整形
    iris_data = DataFrame(x, columns=['Seoal Length', 'Sepal Width', 'Petal Length', 'Petal Width'])
    iris_target = DataFrame(y, columns=['Species'])
    iris_target = iris_target['Species'].apply(change_to_flower_name)
    # print(iris_target.head())

    # -----------------------------↓データの可視化----------------------------------------------
    if True:
        # グラフ描画用に一つのDataFrameにまとめておく
        iris = pd.concat([iris_data, iris_target], axis=1)

        # 分類わけ問題は、"目的変数(Species)で層別することが重要"
        sns.pairplot(iris, hue='Species', size=2)
        plt.show()

        plt.figure(figsize=(12, 4))
        sns.countplot('Petal Length', data=iris, hue='Species')
        plt.show()

    # -----------------------------↓多クラス分類(ロジスティクス回帰)----------------------------------------------
    intercept, coef_df, score = calc_multiple_logistic_classification(iris_data, iris_target, data_split=True)
    print(intercept, coef_df, score)

    # -----------------------------↓多クラス分類(k-近傍法)----------------------------------------------
    knn_model, score = calc_knn(iris_data, iris_target, data_split=True, n_neighbors=6)
    print(score)

    # -----------------------------↓多クラス分類(svm)----------------------------------------------
    svm_model, score = calc_svm(iris_data, iris_target, data_split=True)
    print(score)

    # 境界線描画(⇒描画用に、xを2変数として再学習※し、その結果を描画している)
    # ※3変数以上のmeshを作成できないので！(作成者の実力では)
    svm_model, score = calc_svm(iris_data.iloc[:, :2], y, data_split=True)
    make_2Dgraph_predicted_result(svm_model, iris_data.iloc[:, :2], y)

    # -----------------------------↓多クラス分類(naive_bayes)----------------------------------------------
    svm_model, score = calc_gaussian_naive_bayes(iris_data, iris_target, data_split=True)
    print(score)

    print('fin')

