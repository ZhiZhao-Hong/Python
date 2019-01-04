# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :1/3/2019 3:29 PM
# @Author   :zhong
# @Software :PyCharm
import asyncio
import collections
import aiohttp
import tqdm
from aiohttp import web
from flags.flags2_common import main, HTTPStatus, Result, save_flag


# 默认设为较小的值，防止远程网站出错
# 例如503 - Service Temporarily Unavailable
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000


class FetchError(Exception):

    def __init__(self, country_code):
        self.country_code = country_code


@asyncio.coroutine
def get_flag(base_url, cc: str):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = yield from aiohttp.ClientSession().get(url)
    if resp.status == 200:
        image = yield from resp.read()
    elif resp.status == 404:
        raise web.HTTPNotFound()
    else:
        raise aiohttp.HttpProcessingError(
            code=resp.status, message=resp.reason, headers=resp.headers
        )

@ asyncio.coroutine
def download_one(cc, base_url, semaphore, verbose):
    try:
        with (yield from semaphore):
            image = yield from get_flag(base_url, cc)
    except web.HTTPNotFound:
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        raise FetchError(cc) from exc
    else:
        save_flag(image, cc.lower()+'.gif')
        status = HTTPStatus.ok
        msg = 'OK'
        if verbose and msg:
            print(cc, msg)
    return Result(status, cc)