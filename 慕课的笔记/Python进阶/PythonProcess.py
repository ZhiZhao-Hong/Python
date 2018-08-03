# -*- coding:utf-8 -*-
# 耗cpu的操作, 用多进程编程, 对于io操作来说，使用多线程编程，进程切换代价高于线程
# 1.对于耗费cpu的操作，多进程优于多线程

import time
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures import as_completed

# cpu 操作
def fib(n):
    if n <= 2:
        return 1
    return fib(n-1) + fib(n-2)

if __name__ == '__main__':
    with ProcessPoolExecutor(3) as executor:
        all_task = [executor.submit(fib, (number)) for number in range(25,40)]
        start_time = time.time()
        for future in as_completed(all_task):
            result = future.result()
            print (result)
        print ('总体花费时间：{}'.format(time.time() - start_time))

# io 操作（多线程切换比较快点，进程耗费的内存比较高）
# ----------------------------------------------------------------------------------------------------------------------
from concurrent.futures.process import ProcessPoolExecutor
from multiprocessing import Process, Pool, cpu_count, Queue, JoinableQueue, Manager
import time, multiprocessing


def get_html(n):
    time.sleep(n)
    return n


class MyProgress(Process):
    def run(self):
        pass


if __name__ == '__main__':
    # progress = Process(target=get_html, args=(2,))
    # print (progress.pid)
    # progress.start()
    # print(progress.pid)
    # progress.join()
    # print ('main end')
    #
    # # 使用进程池
    # pool = Pool()
    # pool是使用不了消息队列queue的
    # 要使用Manager().Queue 才可以在pool使用
    pool = Pool(multiprocessing.cpu_count())
    result = pool.apply_async(get_html, args=(3,))
    # 等待所有的任务完成
    pool.close()
    pool.join() # join 之前一定要关闭 ，等待所有的任务都完成
    print (result.get())

    # imap 顺序打印
    for result in pool.imap(get_html, [1, 5, 3]):
        print ("{} result success".format(result))

    # imap_unordered   谁先完成就打印谁
    for result in pool.imap_unordered(get_html, [1, 5, 3]):
        print ("{} result success".format(result))
# ----------------------------------------------------------------------------------------------------------------------
# 管道通讯
# Pipe 的性能高于Queue
import time
from multiprocessing import Pipe, Pool, Process, Manager
from multiprocessing.managers import SyncManager

def producer(queue):
    queue.put("a")
    time.sleep(2)

def consumer(queue):
    time.sleep(2)
    data = queue.get()
    print (data)


if __name__ == '__main__':
    # Pipe 只可以两个进程之间的通讯
    receive_pipe, send_pipe = Pipe()
    pool = Pool(2)
    my_producer = Process(target=producer, args=(send_pipe, ))
    my_consumer = Process(target=consumer, args=(receive_pipe, ))
    my_producer.start()
    my_consumer.start()
    my_producer.join()
    my_consumer.join()

# ----------------------------------------------------------------------------------------------------------------------
# 维护公用变量
from multiprocessing import Manager, Process

def add_data(p_dict, key, value):
    p_dict[key] = value

if __name__ == '__main__':
    progress_dict = Manager().dict()
    first_progress = Process(target=add_data, args=(progress_dict, 'bobby1'))
    second_progress = Process(target=add_data, args=(progress_dict, 'bobby2'))
    first_progress.start()
    second_progress.start()
    first_progress.join()
    second_progress.join()