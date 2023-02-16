#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
    用于发送消息的函数
    :param uid: 用户id
    :param message: 发送的消息
    :param gid: 群id
    :return: None
"""
import asyncio
import httpx
from datetime import datetime
def bl(uid, message):  # 处理私聊信息
    if message:  # 简单的判断，只是判断其是否为空
        asyncio.run(sends(uid, f"{ message }\n回复时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
def handle_private(uid, message):  # 处理私聊信息
    if message:  # 简单的判断，只是判断其是否为空
        asyncio.run(send(uid, f"你好呀，请问发消息给我有什么事情?\n回复时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
def handle_privates(uid, message):  # 处理群聊信息
    if message:
        print(message)
        print('')
        asyncio.run(sends(uid, f"{ message }\n回复时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))


async def send(uid, message, gid=None):
    async with httpx.AsyncClient(base_url="http://127.0.0.1:5700") as client:
        if gid is None:
            # 如果发送的为私聊消息

            params = {
                "user_id": uid,
                "message": message,
            }
        await client.get("/send_private_msg", params=params)
async def sends(uid, message):
    async with httpx.AsyncClient(base_url="http://127.0.0.1:5700") as client:
        params = {
            "group_id": uid,
            "message": message,
            # 'auto_escape': True,
        }
        await client.get("/send_group_msg", params=params)
