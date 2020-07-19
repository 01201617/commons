import requests


def python_notify(line_token, message, *args):
    # 諸々の設定
    line_notify_api = 'https://notify-api.line.me/api/notify'
    line_notify_token = line_token #メモしておいたアクセストークンに置換
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    # メッセージ
    payload = {'message': message}
    # 画像を含むか否か
    if len(args) == 0:
        requests.post(line_notify_api, data=payload, headers=headers)
    else:
        # 画像
        files = {"imageFile": open(args[0], "rb")}
        requests.post(line_notify_api, data=payload, headers=headers, files=files)


if __name__=='__main__':
    line_token = ''
    with open('line_token.txt') as f:
        l = f.readlines()
        line_token = l[0]
    python_notify(line_token, 'co2測定結果です', 'D:/Nan/PycharmProjects/team_development/mainthread_package/co2/png/2020-07-19.png')