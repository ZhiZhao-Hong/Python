# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :1/3/2019 11:43 AM
# @Author   :zhong
# @Software :PyCharm
# yield from foo 句法能防止阻塞。是因为当前协程(即包含yield from 代码的委派生成器)暂停后，
# 控制权回到事件循环手中，再去驱动其他协程。foo futures 或 协程运行完毕后，把结果返回给暂停的协程，将其恢复。

import asyncio
import aiohttp


from flags._flags import BASE_URL, save_flag, show, main


@asyncio.coroutine
def get_flag(cc: str):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = yield from aiohttp.ClientSession().get(url)
    image = yield from resp.read()
    return image


@asyncio.coroutine
def download_one(cc: str):
    image = yield from get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    loop = asyncio.get_event_loop()
    # 调用download_one函数获取各个国旗，然后构建一个生成器对象列表
    to_do = [download_one(cc) for cc in sorted(cc_list)]
    # wait是一个协程，等传给它的所有协程运行完毕之后结束。
    wait_coro = asyncio.wait(to_do)
    # 执行时间循环，知道wait_coro运行结束。
    # 事件循环运行的过程中，这个脚本会在这里阻塞。
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()
    return len(res)


if __name__ == '__main__':
    import time
    main(download_many)