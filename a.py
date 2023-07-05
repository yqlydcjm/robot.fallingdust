import httpx
import os
import asyncio

CQHTTP_HOST = "http://106.54.190.158:55555"
ACCESS_TOKEN = "yM5k84CsxfXzUUAh"


async def send(message: str, *, group_id: int):
    payload = {"group_id": group_id, "message": message}
    async with httpx.AsyncClient(base_url=CQHTTP_HOST) as client:
        if ACCESS_TOKEN is not None:
            client.headers.update({"Authorization": f"Bearer {ACCESS_TOKEN}"})
        response = await client.post("/send_msg", json=payload)
        print(response.json())


async def main():
    while True:
        await send("群主中考打满分", group_id=738458661)
        await asyncio.sleep(10)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("正在退出")
