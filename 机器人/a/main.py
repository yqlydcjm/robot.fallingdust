#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "main.py"
__time__ = "2022/9/9 22:03"

from flask import Flask, request
from flask_restful import Resource, Api
import script

app = Flask(__name__)
api = Api(app)
class AcceptMes(Resource):

    def post(self):
        # 这里对消息进行分发，暂时先设置一个简单的分发
        _ = request.json
        if _.get("message_type") == "private":  # 说明有好友发送信息过来
            uid = _["sender"]["user_id"]  # 获取发信息的好友qq号
            message = _["raw_message"]  # 获取发送过来的消息
            script.handle_private(uid, message)
api.add_resource(AcceptMes, "/", endpoint="index")
if __name__ == '__main__':
    app.run("0.0.0.0", "5701")  # 注意，这里的端口要和配置文件中的保持一致
