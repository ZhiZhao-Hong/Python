# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :1/2/2019 10:08 AM
# @Author   :zhong
# @Software :PyCharm
from concurrent import futures
import os
import sys
import time
import requests


POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = 'downloads/'


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flag(cc: str):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content


def show(text):
    print(text, end=' ')
    sys.stdout.flush()      # 刷新输出


MAX_WORKER = 20


def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    workers = min(MAX_WORKER, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(cc_list))
        # map方法的作用和内置的map函数类似，不过download_one函数会在多个线程中,
        # 并发调用，map方法返回一个生成器，因此可以迭代，获取各个函数返回的值
    return len(list(res))


def download_many_1(cc_list):
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do = []
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc)
            # executor.submit 方法排定可调用对象的执行时间，然后返回一个期物
            # 表示这个待执行的操作
            to_do.append(future)
            # 存储各个期物，后面传给as_completed函数
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc, future))

        results = []
        for future in futures.as_completed(to_do):
            # as_completed 函数在期物运行结束后产出的期物
            res = future.result()
            # 获取预期的产物
            msg = '{} result: {!r}'
            print(msg.format(future, res))
            results.append(res)

    return len(results)


def main():
    t0 = time.time()
    count = download_many_1(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main()
