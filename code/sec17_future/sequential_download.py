"""
    Des：section17 单线程下载
    Date: 2021.06.25
"""
from time import sleep, strftime
from concurrent import futures

def display(*args):
    # print(strftime("%H:%M:%s"))
    print(strftime("[%H:%M:%S]"),end=' ')
    print(*args)

def loiter(n):
    msg = "{} loiter ({}) : doing noting for {} s..."
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = "{} loiter ({}) ：done"
    display(msg.format('\t'*n, n))
    return n*10

# 多线程map 实现
def run_v1():
    display("Script staring")
    # executor = futures.ProcessPoolExecutor(max_workers=4)
    executor = futures.ThreadPoolExecutor(max_workers=3)
    res = executor.map(loiter, range(5))
    display("result:", res)     # result: <generator object _chain_from_iterable_of_lists at 0x7fd024b3e990>
    display("play individual result")
    for i, r in enumerate(res):
        msg = "index : {}, result: {}"
        display(msg.format(i,r))
    display("Script end...")


# run_v1()
"""
[23:07:28] Script staring
[23:07:28]  loiter (0) : doing noting for 0 s...
[23:07:28]  loiter (0) ：done
[23:07:28] 	 loiter (1) : doing noting for 1 s...
[23:07:28] 		 loiter (2) : doing noting for 2 s...
[23:07:28] result: <generator object Executor.map.<locals>.result_iterator at 0x7fae63360a40>
[23:07:28] play individual result
[23:07:28] index : 0, result: 0
[23:07:28] 			 loiter (3) : doing noting for 3 s...
[23:07:29] 	 loiter (1) ：done
[23:07:29] 				 loiter (4) : doing noting for 4 s...
[23:07:29] index : 1, result: 10        # 开始等待 loiter(2) 的result结果，有阻塞可能性
[23:07:30] 		 loiter (2) ：done
[23:07:30] index : 2, result: 20
[23:07:31] 			 loiter (3) ：done
[23:07:31] index : 3, result: 30
[23:07:33] 				 loiter (4) ：done
[23:07:33] index : 4, result: 40
[23:07:33] Script end...
"""
# 使用 submit 和 as_completed 替代map ，进行阻塞优化
def run_v2():
    display("Script staring")
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        todo = []
        for i in range(5):
            future = executor.submit(loiter, i)
            todo.append(future)

        results = []
        for future in futures.as_completed(todo):
            res = future.result()
            msg = "result : {}"
            display(msg.format(res))
            results.append(res)

    for i, r in enumerate(results):
        msg = "index : {}, result: {}"
        display(msg.format(i,r))
    display("Script end...")


from tqdm import tqdm
import requests
from collections import Counter
from fluentPython.future.conf import process_args, save_flag, HTTPStatus, Result, run

DEFAULT_CONCUR_REQ =1
MAX_CONCUR_REQ =1

# seqential
def get_flag(base_utl, cc):
    url = "{}/{cc}/{cc}.gif".format(base_utl,cc = cc.lower())
    resp = requests.get(url)
    if resp.status_code != 200:
        resp.raise_for_status()
    return resp.content

def download_one(cc, base_url, verbose = False):
    try:
        img = get_flag(base_url,cc)
    except requests.exceptions.HTTPError as e:      #下载访问的异常处理
        res = e.response
        if res.status_code == 404:
            status = HTTPStatus.not_found
            msg = "not found"
        else:
            raise
    else:
        save_flag(img, cc.lower()+'.gif')
        status = HTTPStatus.ok
        msg = 'OK'

    if verbose:
        print(cc,msg)

    return Result(status, cc)

def download_many(cc_list, base_url, max_req, verbose=False):
    counter = Counter()
    cc_iter = sorted(cc_list)
    if not verbose:
        cc_iter = tqdm(cc_iter)

    for cc in cc_iter:
        try:
            result = download_one(cc, base_url, verbose)
        except requests.exceptions.HTTPError as exc:
            msg = "HTTP error {result.status} = {result.reason}"
            error_msg = msg.format(result = exc.response)

        except requests.exceptions.ConnectionError as exc:
            error_msg = "Connection error"

        else:
            error_msg = ''
            status = result.status

        counter[status] += 1

        if verbose and error_msg: # <11>
            print('*** Error for {}: {}'.format(cc, error_msg))
    return counter


if __name__ == '__main__':
    run(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
    """
    LOCAL site: http://localhost:8001/flags
    Searching for 676 flags: from AA to ZZ
    1 concurrent connection will be used.
    100%|██████████| 676/676 [00:01<00:00, 390.97it/s]
    --------------------
    194 flags downloaded.
    482 not found.
    Elapsed time: 1.73s
    """

