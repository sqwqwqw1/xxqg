import requests
import os

os.system('clear')

token_url = 'http://localhost:8000/token'
user_dict = {
    'username':'user01',
    'password':'password',
}
r = requests.post(token_url, user_dict)
headers={"Authorization": "Bearer " + r.json()['access_token']}

url = 'http://localhost:8000/xxqg'
# 死循环永远执行
while 1:
    q = input("请输入查询字符：")
    if q=='': 
        os.system('clear') #清空屏幕
        continue
    os.system('clear')  #清空屏幕
    data = {
        'key': q,
    }
    r = requests.post(url, data=data, headers=headers)
    if r.json()['status']=='success':
        li = r.json()['data']

        for i in li:
            print(f"题目：{i['question']}\n答案：{i['answer']}\n\n")
    else:
        print(r.json())