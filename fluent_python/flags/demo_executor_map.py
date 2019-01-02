# /user/bin/python3
# -*- coding:utf-8 -*-
# @Time     :1/2/2019 1:05 PM
# @Author   :zhong
# @Software :PyCharm
from time import sleep, strftime
from concurrent import futures


def display(*args):
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)


def loiter(n):
    msg = '{} loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = '{} loiter({}): done'
    display(msg.format('\t'*n, n))
    return n * 10


def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)
    results = executor.map(loiter, range(5))
    # 把五个任务提交给executor
    # 因为只有3个线程，所以只有3个任务会立即开始，这里是非阻塞调用
    display('results:', results)
    # results是一个生成器
    display('Waiting for individual results:')
    # for循环中的enumerate函数会隐式调用next(result), 这个函数又会在（内部）表示第一个任务的_f期物上调用_f.result()方法。
    # result方法会阻塞，直到期物运行结束，因此这个循环每次迭代时，都要等待下一个结果做好准备。
    for i, result in enumerate(results):
        display('result {}: {}'.format(i, result))


if __name__ == '__main__':
    main()
