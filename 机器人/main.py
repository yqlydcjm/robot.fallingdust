#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from flask import Flask, request
import os
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
    email = db.Column(db.String(36), nullable=True)
    content = db.Column(db.String(36), nullable=False)

class AcceptMes(Resource):

    def post(self):
        # 这里对消息进行分发，暂时先设置一个简单的分发
        _ = request.json
        if _.get("message_type") == "private":  # 说明有好友发送信息过来
            uid = _["sender"]["user_id"]  # 获取发信息的好友qq号
            message = _["raw_message"]  # 获取发送过来的消息

            if uid ==1317497275:
                if message[0:2] == '群发':
                    tool.qf(message)
                else:
                    chatgpt.chat(uid,message)
            else:
                chatgpt.chat(uid,message)
            # chatgpt.chat(uid,message)
        if _.get("message_type") == "group":
            uid = _["group_id"] # 获取发信息的qq群号
            a = _["sender"]["user_id"]  # 
            message = _["raw_message"]  # 获取发送过来的消息
            content = User.query.filter(User.email == a).first()
            # with app.app_context():w 
            if content is None:
                pass
            else:
                content = content.content
            if a == 1317497275:

                script.handle_privates(uid, message,content = content)
            else:
                if '提问' in message:

                    chatgpt.chats(uid, message)

api.add_resource(AcceptMes, "/", endpoint="index")
if __name__ == '__main__':
    with app.app_context():
        db.drop_all()# 删除数据表
        db.create_all()# 创建数据表
    new_user = User(email=1317497275, content='你好，屎壳郎，最近堆屎山了吗')
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()
    app.run("0.0.0.0", "5701")  # 注意，这里的端口要和配置文件中的保持一致
