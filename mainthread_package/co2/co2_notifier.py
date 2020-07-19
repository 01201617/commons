import datetime
import time
import os
import schedule
import pandas as pd
import matplotlib.pyplot as plt

from mainthread_package.co2 import send_png_to_line

def main_job(specific_time):

    df_init, file_name = refresh_df(specific_time)

    # TODO 今後、関数に置き換える予定
    current_co2 = 400
    current_time = "{0:%H:%M}".format(datetime.datetime.now())
    current_df = pd.DataFrame([current_time, current_co2], index=df_init.columns).T
    df_update = df_init.append(current_df)

    os.makedirs('./txt', exist_ok=True)
    df_update.to_csv(file_name, sep=",", index=False)
    # print(file_name, df_update)

    # TODO 指定時刻以降で、画像送信できていない時に、実施
    current_time = datetime.datetime.now()
    current_day = "{0:%Y-%m-%d}".format(current_time)
    png_path = './png/' + current_day + '.png'
    send_flag_path = './flag/' + current_day + '.txt'
    if current_time.hour >= specific_time.hour:
        if not os.path.isfile(send_flag_path) & os.path.isfile(png_path):
            line_token = ''
            with open('line_token.txt') as f:
                l = f.readlines()
                line_token = l[0]
            # png_path = os.path.abspath(png_path)
            send_png_to_line.python_notify(line_token, 'co2測定結果です', png_path)
            # 送れた証拠に、flagファイル作成
            os.makedirs('./flag', exist_ok=True)
            f = open(send_flag_path, "w")
            f.write("fin")
            f.close()


def refresh_df(specific_time):
    current_time = datetime.datetime.now()
    current_day = "{0:%Y-%m-%d}".format(current_time)
    yesterday = "{0:%Y-%m-%d}".format(datetime.datetime.today() - datetime.timedelta(days=1))

    # specific_time 毎朝六時以降かどうか
    # print(current_time.hour , specific_time.hour)
    if current_time.hour >= specific_time.hour:
        # 今日のファイル名あるか?
        file_name = './txt/' + current_day + '.txt'
        if os.path.isfile(file_name):
            df_init = pd.read_table(file_name, sep=",")
        else:
            # 昨日のファイル読み込みor生成
            file_name = './txt/' + yesterday+'.txt'
            if os.path.isfile(file_name):
                # make_graph
                df_graph = pd.read_table(file_name, sep=",")
                make_graph(df_graph)
                file_name = './txt/' + current_day + '.txt'

            # refresh
            df_init = pd.DataFrame(columns=['date', 'co2[ppm]'])

    else:
        # 昨日のファイル読み込みor生成
        file_name = './txt/' + yesterday + '.txt'
        if os.path.isfile(file_name):
            df_init = pd.read_table(file_name, sep=",")
        else:
            df_init = pd.DataFrame(columns=['date', 'co2[ppm]'])

    return df_init, file_name


def make_graph(df):
    fig = plt.figure()
    # Axesを追加
    ax = fig.add_subplot(111)
    ax.scatter(df['date'], df['co2[ppm]'])

    # decoration
    plt.xticks(rotation=70)
    plt.ylim(0, 1500)
    plt.title("co2_detected_by RasberryPi3_{0:%Y-%m-%d}".format(datetime.datetime.now()))
    plt.xlabel("date")
    plt.ylabel("co2[ppm]")
    ax.tick_params(direction="in", length=5)

    os.makedirs('./png', exist_ok=True)
    fig_name = "./png/{0:%Y-%m-%d}.png".format(datetime.datetime.today())
    fig.savefig(fig_name)


if __name__ == '__main__':

    every_min = 10
    what_hour_days_start = 6

    current_time = datetime.datetime.now()
    specific_time = datetime.datetime(current_time.year, current_time.month, current_time.day, what_hour_days_start)
    schedule.every(every_min).minutes.do(main_job, specific_time=specific_time)
    while True:
        schedule.run_pending()
        # ただの無限ループでは無駄がある(1秒間に何度も実行タイミングかチェックする)ため、time.sleepで1秒間のスリープを挿入
        time.sleep(1)