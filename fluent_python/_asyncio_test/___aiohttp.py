# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :1/3/2019 4:36 PM
# @Author   :zhong
# @Software :PyCharm
import aiohttp
import asyncio


async def test():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            print(resp.status)
            print(await resp.text())

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    loop.close()


if __name__ == '__main__':
    main()