"""
    Des：section17 多线程实现
    Date: 2021.06.25
"""

from tqdm import tqdm
import requests
from collections import Counter
from concurrent import futures
from fluentPython.future.conf import process_args, save_flag, HTTPStatus, Result, run

DEFAULT_CONCUR_REQ =4
MAX_CONCUR_REQ =8

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

# 多线程实现
def download_many(cc_list, base_url, concurr_req, verbose=False):
    counter = Counter()
    with futures.ThreadPoolExecutor(concurr_req) as executor:
        todo_map = {}
        for cc in sorted(cc_list):      # 字母大小排序
            # submit 排定可调用对象的执行时间
            future = executor.submit(download_one, cc, base_url, verbose)

            todo_map[future] = cc
        todo_iter = futures.as_completed(todo_map)
        if not verbose:
            # 迭代器没有长度，因此将处理cclist的元素长度作为进度条显示
            todo_iter = tqdm(todo_iter, total=len(cc_list))

        for future in todo_iter:
            try:
                # 返回正常结果与可调用对象在执行过程中捕获的异常
                result = future.result()
            except requests.exceptions.HTTPError as exc:
                msg = "HTTP error {result.status} = {result.reason}"
                error_msg = msg.format(result = exc.response)
            except requests.exceptions.ConnectionError as exc:
                error_msg = "Connection error"

            else:
                error_msg = ''
                status = result.status
            if error_msg:
                status = HTTPStatus.error
            counter[status] += 1

            if verbose: # <11>
                cc = todo_map[future]
                print('*** Error for {}: {}'.format(cc, error_msg))
    return counter

if __name__ == '__main__':
    run(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
    """
    LOCAL site: http://localhost:8001/flags
    Searching for 676 flags: from AA to ZZ
    5 concurrent connections will be used.
    100%|██████████| 676/676 [00:01<00:00, 583.85it/s]
    --------------------
    194 flags downloaded.
    482 not found.
    Elapsed time: 1.17s
    """


