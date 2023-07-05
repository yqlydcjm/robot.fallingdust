#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "一千零一点"
__file__ = "script.py"
__time__ = "2023/7/1 20:05"

import asyncio
import httpx
from datetime import datetime

# 处理私聊信息
def handle_private(uid, message): # uid为要发送给谁的qq号，message为信息
    print(message)
    asyncio.run(send(uid, f"{message}\n回复时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
# 处理群聊信息
def handle_privates(uid, message): # uid为群号，message为消息
    print(message)
    asyncio.run(sends(uid, f"{ message }\n回复时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
# 如果发送的为私聊消息
async def send(uid, message):
    async with httpx.AsyncClient(base_url="http://127.0.0.1:5700") as client:
        params = {
            "user_id": uid,
            "message": message,
        }
        await client.get("/send_private_msg", params=params)
# 如果发送的为群聊消息
async def sends(uid, message):
    async with httpx.AsyncClient(base_url="http://127.0.0.1:5700") as client:
        params = {
            "group_id": uid,
            "message": message,
        }
        response = await client.post("/send_msg", params=params)
# 测试
if __name__ == '__main__':
    # smash(1317497275)
    # bmi(6, 6, 70,1.70)
    import tool
    handle_privates(738458661, 'tool.today()')