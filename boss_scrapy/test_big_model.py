'''
Author: galeliu
Date: 2024-09-13 17:12:44
LastEditTime: 2024-09-13 17:15:33
LastEditors: galeliu
Description: .
'''
import requests
import uuid

api_key = "286bd4c2e06eac46c294180fbeca3948.J0y2r3whdNUzfC4a"


def run_v4_sync():
    msg = [
        {
            "role": "user",
            "content": "从高德地图上诚民村镇银行华阳支行大堂的电话是多少？"
        }
    ]
    tool = "web-search-pro"
    url = "https://open.bigmodel.cn/api/paas/v4/tools"
    request_id = str(uuid.uuid4())
    data = {
        "request_id": request_id,
        "tool": tool,
        "stream": False,
        "messages": msg
    }

    resp = requests.post(
        url,
        json=data,
        headers={'Authorization': api_key},
        timeout=300
    )
    print(resp.content.decode())


if __name__ == '__main__':
    run_v4_sync()
