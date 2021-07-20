"""
    Des：python asyncio_18 asyncio_18 协程实现国旗下载
    Date: 2021.05.17
"""
import asyncio
import aiohttp
import sys
from fluentPython.future.conf import save_flag, run, ROOT_DIR, DEST_DIR

BASE_URL = 'http://localhost:8001/flags'

class FutureError(Exception):
    def __init__(self, cc):
        self.country_code = cc


def show(cc):
    print(cc, end=' ')
    sys.stdout.flush()

@asyncio.coroutine
def get_flag(base_url, cc):
    img_url = base_url + "/{cc}/{cc}.gif"
    resp = yield from aiohttp.request('GET',url=img_url.format(cc=cc))
    img = yield from resp.read()
    return img

@asyncio.coroutine
def download_one(base_url, cc):
    image = get_flag(base_url, cc)
    save_flag(image, cc.lower()+'.gif')
    return cc

def download_many(cc_list):
    # 建立事件索引
    loop = asyncio.get_event_loop()
    # 构建协程集合
    todo = [download_one(BASE_URL, cc) for cc in sorted(cc_list)]
    wait_coro =asyncio.wait(todo)       #等待所有协程运行完毕后结束，但无法通过进度条查看逐个结果
    result = loop.run_until_complete(wait_coro)
    loop.close()
    return len(result)

