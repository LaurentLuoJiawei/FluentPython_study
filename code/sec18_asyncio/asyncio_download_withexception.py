"""
    Des：python asyncio_18 asyncio_18 协程实现带有异常处理的国旗下载脚本
    Date: 2021.05.17
"""
import asyncio
import aiohttp
from aiohttp import web
import sys
from tqdm import tqdm
from collections import Counter
from fluentPython.future.conf import save_flag, run, HTTPStatus, Result


DEFAULT_CONCUR_REQ = 10
MAX_CONCUR_REQ =1000
VERBOSE = False
BASE_URL = 'http://localhost:8001/flags'

class FetchError(Exception):
    def __init__(self, cc):
        self.country_code = cc


def show(cc):
    print(cc, end=' ')
    sys.stdout.flush()


async def get_flag(base_url, cc):
    img_url = base_url + "/{cc}/{cc}.gif"
    # resp = yield from aiohttp.request('GET',url=img_url.format(cc=cc.lower()))
    # resp = await aiohttp.ClientSession.get(url=img_url.format(cc=cc.lower()))

    async with aiohttp.ClientSession() as session:
        resp = await session.get(url=img_url.format(cc=cc.lower()))
        if resp.status == 200:
            img = await resp.read()
            return img
        elif resp.status == 404:
            raise web.HTTPNotFound()
        else:
            raise aiohttp.ClientError(
                code = resp.status, message=resp.reason, header=resp.headers
            )



async def download_one(base_url, cc, semaphore, verbose):
    try:
        async with  semaphore:
            image = await get_flag(base_url, cc)
    except web.HTTPNotFound:
        # 处理getflag 抛出的异常
            status = HTTPStatus.not_found
            msg = 'not Found'
    except Exception as exc:
        raise FetchError(cc) from exc
    else:
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, save_flag, image, cc.lower()+'.gif')

        # save_flag(image, cc.lower()+'.gif')     # 对
        status = HTTPStatus.ok
        msg = 'ok'
    if verbose:
        print("cc: {} status: {}".format(cc, msg))

    return Result(status,cc)

async def download_coro(cc_list, base_url, verbose, concur_req):
    counter = Counter()
    semaphore = asyncio.Semaphore(concur_req)
    # 封装协程，在协程中中加入semaphore 控制并发数量
    todo = [download_one(base_url, cc, semaphore, verbose) for cc in sorted(cc_list)]
    # 构建task 实例
    todo_iter = asyncio.as_completed(todo)
    if not verbose:
        todo_iter = tqdm(todo_iter, total=len(cc_list))

    for future in todo_iter:
        try:
            res = await future
        except FetchError as excp:
            country_code = excp.country_code
            try:
                # 从原来的异常获取错误信息
                # error_msg = exc.__cause__.args[0]
                error_msg = 'error level one: {}'.format(excp)
            except IndexError as e:
                # error_msg = e.__cause__.__class__
                error_msg = "error level two {}".format(e)
            if verbose and error_msg:
                print("*** Error for {}: {}".format(country_code, error_msg))
                # 如果异常中没有错误信息，则返回异常的类名作为错误消息
            status = HTTPStatus.error
        else:
            status = res.status
            msg = ''
        counter[status] += 1
    return counter


def download_many(cc_list, base_url, max_concur_req):
    # 建立事件索引
    loop = asyncio.get_event_loop()
    # 构建协程集合
    coro = download_coro(cc_list,base_url, VERBOSE, max_concur_req)
    result = loop.run_until_complete(coro)
    loop.close()
    return result

if __name__ == '__main__':
    run(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
    """
    LOCAL site: http://localhost:8001/flags
    Searching for 676 flags: from AA to ZZ
    10 concurrent connections will be used.
    100%|██████████| 676/676 [00:00<00:00, 750.57it/s]
    --------------------
    194 flags downloaded.
    482 not found.
    Elapsed time: 0.92s
    """