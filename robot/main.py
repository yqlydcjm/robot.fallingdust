#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from flask import Flask, request
import os
import threading
from flask_restful import Resource, Api
import script
from flask_sqlalchemy import SQLAlchemy
import tool
import chatgpt
app = Flask(__name__)
api = Api(app)
# 配置数据库
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

class AcceptMes(Resource):

    def post(self):
        # 这里对消息进行分发，暂时先设置一个简单的分发
        _ = request.json
        if _.get("message_type") == "private":  # 说明有好友发送信息过来
            uid = _["sender"]["user_id"]  # 获取发信息的好友qq号
            message = _["raw_message"]  # 获取发送过来的消息

            if uid ==:#机器人主的qq号
                if message[0:2] == '群发':
                    tool.qf(message)
                else:
                    chatgpt.chat(uid,message)
            else:
                t = threading.Thread(target=chatgpt.chat, args=(uid,message,))
                t.start()
            # chatgpt.chat(uid,message)
        if _.get("message_type") == "group":
            uid = _["group_id"] # 获取发信息的qq群号
            a = _["sender"]["user_id"]  # 获取发送者qq号
            message = _["raw_message"]  # 获取发送过来的消息
            content = User.query.filter(User.email == a).first()
            if content is None:
                pass
            else:
                content = content
            if a == '':#主人qq号
                if '提问' in message:
                    t = threading.Thread(target=chatgpt.chats, args=(uid,message,))
                    t.start()
                if '历史上的今天' in message:
                    print(tool.today())
                    script.handle_privates(uid, tool.today())
                else:
                    # script.handle_privates(uid, content.content)
                    pass
                    # script.handle_privates(uid, '黑桃大王八')
            else:
                if '提问' in message:
                    t = threading.Thread(target=chatgpt.chats, args=(uid,message,))
                    t.start()
                if '历史上的今天' in message:
                    script.handle_privates(uid, tool.today())
                if message[0] == '捣':
                    message = int(message[2:])
                    tool.smash(uid, message)
                if message[0:3] == 'bmi':
                    a,b,c = message.split(' ')
                    b = float(b)
                    c = float(c)
                    tool.bmi(uid, b, c)
        # if _.get()



api.add_resource(AcceptMes, "/", endpoint="index")
if __name__ == '__main__':
    with app.app_context():
        db.drop_all()# 删除数据表
        db.create_all()# 创建数据表
    # new_user = User(email=qq, content='黑桃大王八')
    # new_user = User(email=qq, content='你好，屎壳郎，最近堆屎山了吗')
    # with app.app_context():
    #     db.session.add(new_user)
    #     db.session.commit()
    app.run("0.0.0.0", "5701")  # 注意，这里的端口要和配置文件中的保持一致
