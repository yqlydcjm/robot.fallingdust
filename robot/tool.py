import requests
import script
# 群发助手
def qf(uid,message):
    friend_list = requests.get(url='http://127.0.0.1:5700/get_friend_list')
    friends = friend_list.json()
    for i in friends['data']:       #获取用户用户名以及qq号
        uid = i['user_id']
        script.bl(uid, message)
# 历史上的今天
def today():
    today = 'https://api.iculture.cc/api/lishi'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
    html = requests.get(today, headers=headers)
    return html.text
def smash(uid, qq):
    qq = qq
    smash = f'https://api.iculture.cc/api/face_pound/?QQ={qq}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
    html = requests.get(smash, headers=headers)
    r = html.content
    url = f'./img/{qq}_dog.gif'
    with open(url,"wb") as f:
        f.write(r)
    # script.handle_privates(464325726,  f'[CQ:at,qq=2556689087]')

    script.handle_privates(uid,  f'[CQ:image,file=file:///{url}]')
    return url
def bmi(uid, weight, height):
    bmi = weight / pow(height, 2)
    print(bmi)
    if bmi <=18.5:
        content = f'你的bmi值是{bmi},你的体重太低了快多吃点吧！'
    # if bmi <=23.9 and bmi >18.5:
    if 18.5<bmi<23.9:
        content = f'你的bmi值是{bmi},你的体重很标准保持住！'
    if 23.9<=bmi:
        content = f'你的bmi值是{bmi},你太重了，少吃点吧没事多注意锻炼哦'
    script.handle_privates(uid,  content)
if __name__ == '__main__':
    pass