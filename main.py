#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "一千零一点"
__file__ = "main.py"
__time__ = "2023/7/1 20:05"
# test
import os
import websocket
import json
import threading
import script
import tool
import chatgpt
# 配置数据库
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"\
    + os.path.join(basedir, 'database.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
# 用户表
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.Integer(), nullable=True)
    content = db.Column(db.String(36), nullable=False)
def on_message(ws, message):
    _ = json.loads(message)
    post_type = _.get('post_type')
    message_type = _.get('message_type')
    # 消息
    if post_type == 'message':
        if message_type == 'private':
            # print(f"私聊消息：{message}，发送者ID：{user_id}")
            uid = _.get('user_id') # 发送者qq号
            message = _.get('message') # 获取发来的消息
            if uid == 1317497275: #你的QQ号
                if message[0:2] == '群发':
                    t = threading.Thread(target=tool.qf, args=(uid,message,))
                    t.start()
                if '1' in message:
                    t = threading.Thread(target=script.handle_private, args=(uid,message,))
                    t.start()
                else:
                    chatgpt.chat(uid,message)
            else:
                t = threading.Thread(target=chatgpt.chat, args=(uid,message,))
                t.start()
            # chatgpt.chat(uid,message)
        elif message_type == 'group':
            uid = _.get('group_id') # qq群号
            user = _.get('user_id') # 发送者qq号
            message = _.get('message') # 获取发来的消息
            # script.handle_privates(uid, message) # 复读
            # with app.app_context():
            #     content = User.query.filter(User.email == 1317497275).first()
            #     print(content.content)
            if '提问' in message:
                t = threading.Thread(target=chatgpt.chats, args=(uid,message,))
                t.start()
            if '历史' in message:
                script.handle_privates(uid, tool.today())
            if message[0] == '捣':
                message = int(message[2:])
                tool.smash(uid, message)
            if message[0:3] == 'bmi':
                a,b,c = message.split(' ')
                b = float(b)
                c = float(c)
                tool.bmi(uid, b, c)
            if message == '周周周':
                script.handle_privates(uid, "周周周别玩了啊")
            if message == '滚':
                script.handle_privates(uid, "滚就滚，谁怕谁啊")
            if message == '你':
                script.handle_privates(uid, "啊？我咋的了")
            if message == '对':
                script.handle_privates(uid, "啊对对对")
            if message == '等着':
                script.handle_privates(uid, "行，你等着啊")
            if message == '四班':
                script.handle_privates(uid, "咱们四班的孩子啊，就不一般，一盘散沙一样，迟早倒数第一")
            if message == '[CQ:face,id=277]':
                script.handle_privates(uid, "打歪你的狗头")
            if message == '一二三四':
                script.handle_privates(uid, "四四四四")
            if '菠萝' in message:
                script.handle_privates(uid, "菠萝哥捞捞")

    # 收到了事件
    elif post_type == 'event':
        event = _.get('event')
        print(f"收到事件消息：{event}")
        pass

if __name__ == "__main__":
    # with app.app_context():
    #     db.drop_all()# 删除数据表
    #     db.create_all()# 创建数据表
    # new_user = User(email=3234623244, content='黑桃大王八')
    # new_user = User(email=1317497275, content='你好，屎壳郎，最近堆屎山了吗')
    # with app.app_context():
    #     db.session.add(new_user)
    #     db.session.commit()
    ws = websocket.WebSocketApp("ws://localhost:8080/event",
                                on_message=on_message)
    ws.run_forever()