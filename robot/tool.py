import requests
import script
def qf(uid,message):
    friend_list = requests.get(url='http://127.0.0.1:5700/get_friend_list')
    friends = friend_list.json()
    for i in friends['data']:       #获取用户用户名以及qq号
        uid = i['user_id']
        script.bl(uid, message)
