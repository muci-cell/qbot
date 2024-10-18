import asyncio
import json

import requests
from aiohttp import web

from config import *


async def handle_post(request):
    try:
        data = await request.json()  # 解析 JSON 数据
        # 检查 message_type 是否为 "group"
        if data.get("message_type") == "group":
            raw_message = data.get("raw_message")
            group_id = data.get("group_id")

            # 确保 raw_message 是字符串，group_id 是整数
            if isinstance(raw_message, str) and isinstance(group_id, int):
                # 检查 raw_message 是否包含“老师”
                if "老师" in raw_message:
                    # 找到“老师”的索引
                    index = raw_message.index("老师")
                    # 提取“老师”之前最多 5 个字符
                    extracted_text = raw_message[max(0, index - 5):index]
                    print(f"Extracted Text Before '老师': {extracted_text}")

                    payload = {
                        "query": extracted_text
                    }
                    response = requests.post(URL_SEARCH, json=payload)

                    if response.status_code == 200:
                        response_data = response.json()
                        json_str = json.dumps(response_data, ensure_ascii=False)
                        print(json_str)
                        requests.post(URL_SEND, json={
                            'group_id': group_id,
                            'message': [{
                                'type': 'text',
                                'data': {
                                    'text': json_str
                                }
                            }]
                        })


        return web.Response(text="Received POST JSON data successfully")
    except Exception as e:
        print(f"Error processing POST request: {e}")
        return web.Response(status=400, text=f"Error: {e}")


async def init_server():
    app = web.Application()
    app.add_routes([web.post('/', handle_post)])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    print(f"Server started at http://localhost:8080")

    try:
        while True:
            await asyncio.sleep(3600)  # 持续运行，直到手动停止
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(init_server())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
