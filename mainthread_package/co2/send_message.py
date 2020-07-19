import requests

url = ''
with open('line_token.txt') as f:
    l = f.readlines()
    url = l[0]
# url = 'https://script.google.com/macros/s/AKfycbw5rphstUpq_X1JzBiwHQ50sI5qp8dvInLmkMUoeUGC64bQhgc/exec'
data1 = '第２弾：ラズベリーパイからのお知らせ'
data2 = 'パラメータによるテストメールです。'

requests.get(url + '?data1=' + data1 + '&data2=' + data2)