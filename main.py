#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "一千零一点"
__file__ = "main.py"
__time__ = "2023/7/1 20:05"
import json
# test
import os
import threading

import websocket
from flask import Flask
# 配置数据库
from flask_sqlalchemy import SQLAlchemy
import script
import tool

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


# test
# 用户表
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.Integer(), nullable=True)
    content = db.Column(db.String(100), nullable=False)


#   
class Contents(db.Model):
    __tablename__ = "contents"
    id = db.Column(db.Integer(), primary_key=True)
    knowledge = db.Column(db.Integer(), nullable=True)
    content = db.Column(db.String(100), nullable=False)


# 好感表
class Impressions(db.Model):
    __tablename__ = "impressions"
    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.Integer(), nullable=True)
    name = db.Column(db.String(36), nullable=False)
    impression = db.Column(db.Integer(), nullable=False)


def a(message):
    with app.app_context():
        content = Contents.query.filter(Contents.knowledge == message).first()
        return content


def read():
    # 定义文件路径
    file_path = "content.txt"  # 将"path/to/your_file.txt"替换为你的文件路径
    # 尝试打开文件并读取内容
    try:
        with open(file_path, "r") as file:
            content = int(file.read())
            print(content)
            return content
    except FileNotFoundError:
        print("文件未找到，请确认文件路径是否正确。")
    except Exception as e:
        print("读取文件时出现错误:", e)


def on_message(ws, message):
    _ = json.loads(message)
    post_type = _.get("post_type")
    message_type = _.get("message_type")
    # 消息
    if post_type == "message":
        if message_type == "private":
            # print(f"私聊消息：{message}，发送者ID：{user_id}")
            uid = _.get("user_id")  # 发送者qq号
            message = _.get("message")  # 获取发来的消息
            if uid == 1317497275:  # 你的QQ号
                if message == "群发":
                    t = threading.Thread(
                        target=tool.qf,
                        args=(
                            uid,
                            message,
                        ),
                    )
                    t.start()
        elif message_type == "group":
            uid = _.get("group_id")  # qq群号
            user = _.get("user_id")  # 发送者qq号
            message = _.get("message")  # 获取发来的消息
            # script.handle_privates(uid, message) # 复读
            with app.app_context():
                Content = Contents.query.filter(Contents.knowledge == message).first()
            if Content is not None:
                if message == Content.knowledge:
                    script.handle_privates(uid, Content.content)
            else:
                if message[0:3] == "bmi":
                    a, b, c = message.split(" ")
                    b = float(b)
                    c = float(c)
                    tool.bmi(uid, b, c)
                if message[0:2] == "教学":
                    a, b, c = message.split(" ")
                    new_user = Contents(knowledge=b, content=c)
                    with app.app_context():
                        db.session.add(new_user)
                        db.session.commit()
                    script.handle_privates(uid, "教学成功")
                if message[0:4] == "删除教学":
                    a, b = message.split(" ")
                    with app.app_context():
                        new_user = Contents.query.filter(
                            Contents.knowledge == b
                        ).first()
                        db.session.delete(new_user)
                        db.session.commit()
                    script.handle_privates(uid, "删除成功")
                if message[0:3] == "给管理":
                    a, b = message.split(" ")
                    tool.admin_gave(uid, b)
                    script.handle_privates(uid, f"已添加{b}为群管理")
                if message[0:3] == "删管理":
                    a, b = message.split(" ")
                    tool.admin_get(uid, b)
                    script.handle_privates(uid, f"已删除{b}群管理")
                if message == "开群":
                    tool.group_open(uid)
                    script.handle_privates(uid, "已关闭本群全体禁言")
                if message == "关群":
                    tool.group_close(uid)
                    script.handle_privates(uid, "已开启本群全体禁言")
                if message[0:2] == "禁言":
                    a, b, c = message.split(" ")
                    tool.user_ban(uid, b, c)
                    if c == 0:
                        script.handle_privates(uid, f"已解禁{b}")
                    else:
                        script.handle_privates(uid, f"已禁言{b}{c}秒")
                if message[0:3] == "给头衔":
                    a, b, c = message.split(" ")
                    tool.title(uid, b, c)
                    script.handle_privates(uid, f"已赠{user}头衔{c}")
                if message[0:2] == "注册":
                    a, b = message.split(" ")
                    with app.app_context():
                        test = Impressions.query.filter(
                            Impressions.user == user
                        ).first()
                    print(test)
                    if test is not None:
                        script.handle_privates(uid, f"你({test.name})注册过了,一边眯着去")
                    else:
                        new_user = Impressions(user=user, name=b, impression=0)
                        with app.app_context():
                            db.session.add(new_user)
                            db.session.commit()
                        script.handle_privates(uid, f"{b}注册成功")
                if message[0:2] == "签到":
                    with app.app_context():
                        test = Impressions.query.filter(
                            Impressions.user == user
                        ).first()
                        # print(type(test))
                        # print(test.impression)
                        test.impression = test.impression + read()
                        db.session.commit()
                        script.handle_privates(uid, f"签到成功，你目前的好感值是{test.impression}")

                # if message == '周周周':
                #     script.handle_privates(uid, "周周周别玩了啊")
                # if message == '滚':
                #     script.handle_privates(uid, "滚就滚，谁怕谁啊")
                # if message == '你':
                #     script.handle_privates(uid, "啊？我咋的了")
                # if message == '等着':
                #     script.handle_privates(uid, "行，你等着啊")
                # if message == '四班':
                #     script.handle_privates(uid, "咱们四班的孩子啊，就不一般，一盘散沙一样，迟早倒数第一")
                # # if message == '[CQ:face,id=277]':
                # if message == '/汪汪':
                #     script.handle_privates(uid, "打歪你的狗头")
                # if message == '一二三四':
                #     script.handle_privates(uid, "四四四四")
                # if '菠萝' in message:
                #     script.handle_privates(uid, "菠萝哥捞捞")

                else:
                    with app.app_context():
                        content = User.query.filter(User.email == user).first()
                    if user == content.email:
                        script.handle_privates(uid, content.content)

    # 收到了事件
    elif post_type == "event":
        event = _.get("event")
        print(f"收到事件消息：{event}")
        pass


if __name__ == "__main__":
    # with app.app_context():
    #     db.drop_all()# 删除数据表
    #     db.create_all()# 创建数据表
    # new_user = User(email=550341836, content='老八')
    # with app.app_context():
    #     db.session.add(new_user)
    #     db.session.commit()
    # new_user = Contents(knowledge='周周周', content='周周周别玩了啊')
    # with app.app_context():
    #     db.session.add(new_user)
    #     db.session.commit()
    print('运行开始')
    ws = websocket.WebSocketApp("ws://localhost:8080/event", on_message=on_message)
    ws.run_forever()
