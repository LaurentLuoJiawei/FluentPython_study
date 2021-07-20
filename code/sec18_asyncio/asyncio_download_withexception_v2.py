"""
    Des：python asyncio_18 asyncio_18 协程实现每次下载多次请求
    Date: 2021.05.17
"""
import asyncio
import aiohttp
from aiohttp import web
import sys
from tqdm import tqdm
from collections import Counter
from fluentPython.future.conf import save_flag, run, HTTPStatus, Result


"""
在文件保存时，使用国家名和代码，因此下载时发起两个请求，一个用于获取国旗，另一个用于获取图像在目录中的文件名
"""

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

async def http_get(url):
    async with aiohttp.ClientSession() as session:
        res = await session.get(url)
        if res.status == 200:
            content_type = res.content_type.lower()
            if 'json' in content_type or content_type.endswith('json'):
                data = await res.json()
            else:
                data = await res.read()
            return data
        elif res.status == 404:
            raise web.HTTPNotFound
        else:
            raise aiohttp.ClientError(
                message = res.reason, header= res.headers, code = res.status
            )


async def get_flag(base_url, cc):
    img_url = '{url}/{cc}/{cc}.gif'.format(url=base_url, cc=cc.lower())
    response = await http_get(img_url)
    return response

async def get_country(base_url, cc):
    country_code_url = '{url}/{cc}/metadata.json'.format(url=base_url, cc=cc.lower())
    response = await http_get(country_code_url)
    return response['country']

async def download_one(base_url, cc, semaphore, verbose):
    try:
        async with semaphore:
            image = await get_flag(base_url, cc)
            # country_name = await get_country(base_url,cc)

        async with semaphore:
            country_name = await get_country(base_url,cc)

    except web.HTTPNotFound:
        # 处理getflag 抛出的异常
            status = HTTPStatus.not_found
            msg = 'not Found'
    except Exception as exc:
        raise FetchError(cc) from exc
    else:
        country_name = country_name.replace(' ','_')
        filename = cc.lower() + country_name + '.gif'
        # img = 'sdfsdf'
        # filename = cc.lower() + '11' + '.gif'
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, save_flag, image, filename)      #将普通阻塞型函数委托给线程池
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
    100%|██████████| 676/676 [00:01<00:00, 610.59it/s]
    --------------------
    194 flags downloaded.
    482 not found.
    Elapsed time: 1.12s
    """