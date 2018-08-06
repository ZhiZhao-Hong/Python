# -*- coding:utf-8 -*-

# gil = global interpreter lock
'''
python 中一个线程对应于C语言中的一个线程
gil使得同一时刻只有一个线程运行在一个cpu上执行字节码, 无法将多个线程映射到多个cpu上执行

gil 会根据执行的字节码的函数以及时间片释放gil，或者在io操作的时候，会释放
'''
#-----------------------------------------------------------------------------------------------------------------------
# 字节码编程
import dis
def add(a):
    a = a + 1
    return a
print (dis.dis(add))


# ---------------------------------------------------------------------------------------------------------------------
# 哪怕有GIL锁，也是不安全的
total = 0

def add():
    global total
    for i in range(1000000):
        total += 1

def desc():
    global total
    for i in range(1000000):
        total -= 1

import threading
thread1 = threading.Thread(target=add)
thread2 = threading.Thread(target=desc)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print (total)

#-----------------------------------------------------------------------------------------------------------------------
# 对于io操作来说，多线程和多进程性能差别不大
# 多线程爬虫

# 第一种写法 - 代码量少的时候可以这样使用
import time,threading
def get_detail_html(url):
    print ("get detail html started")
    time.sleep(2)
    print ("get detail html end")


def get_detail_url(url):
    print ("get detail url started")
    time.sleep(2)
    print ("get_detail url end")

if __name__ == '__main__':
    # 运行的也是一个主线程，thread1和thread2也都是线程
    thread1 = threading.Thread(target=get_detail_html, args=("",))
    thread2 = threading.Thread(target=get_detail_url, args=("",))

    # 守护线程, True的时候，主线程关闭，子线程全部关闭，反正为False的时候，会等待子线程结束之后才结束
    thread1.setDaemon(True)
    thread2.setDaemon(True)

    start_time = time.time()
    thread1.start()
    thread2.start()

    # 线程阻塞 - 等thread1和2 都阻塞完成之后，才会往下运行
    thread1.join()
    thread2.join()

    print ("last time:{}".format(time.time()-start_time))


# 第二种写法 - 通过继承
import threading,time
class GetDetailHtml(threading.Thread):

    def __init__(self, name):
        super().__init__(name=name)

    def run(self):
        print ("get detail html started")
        time.sleep(2)
        print ("get detail html end")


class GetDetailUrl(threading.Thread):

    def __init__(self, name):
        super().__init__(name=name)

    def run(self):
        print ("get detail url started")
        time.sleep(2)
        print ("get_detail url end")

if __name__ == '__main__':
    thread1 = GetDetailHtml("")
    thread2 = GetDetailUrl("")
    thread1.start()
    thread2.start()
# ----------------------------------------------------------------------------------------------------------------------

# 线程之间的通讯
import time,threading
from queue import Queue
def get_detail_html(queue):
    """获取详情页面"""
    while True:
        # 如果拿到的为空，会一直停在这里
        url = queue.get()
        print ("get detail html started")
        time.sleep(2)
        print (url)
        print ("get detail html end")
        queue.task_done()


def get_detail_url(queue):
    """获取文章的列表页"""
    print ("get detail url started")
    for i in range(10):
        queue.put("test{id}".format(id=i))
        time.sleep(2)
    print ("get_detail url end")

# 1. 共享变量来控制 - 多线程  (不安全)
# 2. queue 安全队列进行线程同步 (消息队列)

if __name__ == '__main__':

    detail_url_queue = Queue()
    thread1 = threading.Thread(target=get_detail_url, args=(detail_url_queue,))
    thread2 = threading.Thread(target=get_detail_html, args=(detail_url_queue,))

    thread1.start()
    thread2.start()

    thread1.join()

    # 消息队列接受到task_done 发送过来的指令之后们就会结束
    detail_url_queue.join()
    print ('1')

# ----------------------------------------------------------------------------------------------------------------------
from queue import Queue
from threading import Thread,Event
from io import StringIO
from bs4 import BeautifulSoup
import requests,openpyxl

class IOThread(Thread):
    def __init__(self,i,Queue):
        Thread.__init__(self)
        self.sid = i
        self.url = 'https://www.52pojie.cn/forum-16-{0}.html'.format(i)
        self.queue = Queue

    def download(self,url):
        print ('%s：已完成' % str(self.sid))
        response = requests.get(url,timeout=3)
        if response.ok:
            return StringIO(response.text)

    def run(self):
        data = self.download(self.url)
        self.queue.put((self.sid,data))

class CpuThread(Thread):
    def __init__(self,queue,cEvent,tEvent):
        Thread.__init__(self)
        self.queue = queue
        self.cEvent = cEvent
        self.tEvent = tEvent

    def test(self,sid,data):
        html = BeautifulSoup(data.read(),'lxml')
        url = html.select('th.new > a.s.xst')
        print (url)

    def run(self):
        count = 0
        while True:
            sid,data = self.queue.get()
            print (sid,data)
            if sid == '-1':
                self.cEvent.set()
                self.tEvent.wait()
                break
            if data:
                self.test(sid,data)
                count +=1
                if count == 5:
                    self.cEvent.set()
                    self.tEvent.wait()
                    self.tEvent.clear()
                    count = 0

class zipThread(Thread):
    def __init__(self,cEvent,tEvent):
        Thread.__init__(self)
        self.count = 0
        self.cEvent = cEvent
        self.tEvent = tEvent
        self.setDaemon(True)

    def zip_print(self):
        print('打包完成')

    def run(self):
        while True:
            self.cEvent.wait()
            self.zip_print()
            self.cEvent.clear()

            self.tEvent.set()

if __name__ == '__main__':
    q = Queue()
    dThreads = [IOThread(i,q) for i in range(1,18)]
    cEvent = Event()
    tEvent = Event()
    cThreads = CpuThread(q,cEvent,tEvent)
    tThreads = zipThread(cEvent,tEvent)
    tThreads.start()

    for t in dThreads:
        t.start()
    cThreads.start()

    for t in dThreads:
        t.join()

    q.put(('-1',None))


# ----------------------------------------------------------------------------------------------------------------------
# 线程同步

# 全局变量在赋值的时候，容易出错，运算完成之后，复制别的线程先赋值
# 同时操作数据库时候，只允许只有一个代码段在运行

# 锁会影响性能
# 锁是引起死锁
# 1. 资源竞争 解决办法：获取的资源的顺序要一致
# 2. 函数嵌套

'''
lock.acquire()
lock.acquire()
lock.release()
lock.release()

这样就会变成死锁，第二个acquire会等待第一个释放，但是第一个释放不了

RLock就可以改变这个情况
'''

from threading import Lock
total = 0
lock = Lock()   # 消耗性能

def add():
    global total
    for i in range(1000000):
        lock.acquire()  # 加锁
        total += 1
        lock.release()  # 释放

def desc():
    global total
    for i in range(1000000):
        lock.acquire()  # 加锁
        total -= 1
        lock.release()  # 释放

import threading
thread1 = threading.Thread(target=add)
thread2 = threading.Thread(target=desc)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print (total)

# ----------------------------------------------------------------------------------------------------------------------
# Condition 可以控制复杂的网络通讯 - lock的高级使用
import threading
from threading import Condition, Semaphore

class XiaoAi(threading.Thread):

    def __init__(self, cond):
        self.cond = cond
        super().__init__(name="小爱")

    def run(self):
        with self.cond:
            self.cond.wait()
            print (" {} : 在".format(self.name))
            self.cond.notify()

            self.cond.wait()
            print(" {} : 好呀！".format(self.name))
            self.cond.notify()

class TianMao(threading.Thread):

    def __init__(self, cond):
        self.cond = cond
        super().__init__(name="天猫精灵")

    def run(self):
        with self.cond:
            print (" {} : 小爱同学".format(self.name))
            self.cond.notify()
            self.cond.wait()

            print(" {} : 我们来对古诗吧。".format(self.name))
            self.cond.notify()
            self.cond.wait()

if __name__ == '__main__':
    cond = Condition()
    thread1 = XiaoAi(cond)
    thread2 = TianMao(cond)
    thread1.start()
    thread2.start()

# ----------------------------------------------------------------------------------------------------------------------
# Semaphore 是用于控制进入数量的锁
# - 文件  读、写  写一般只是用于一个线程写，读可以允许有多个
# - 爬虫

import threading, time

class HtmlSpider(threading.Thread):

    def __init__(self, sem):
        super().__init__()
        self.sem = sem

    def run(self):
        time.sleep(2)
        print (" got html text success")
        self.sem.release() # 子线程释放一次，semaphore设定的数量加一， 当为3的时候，self.sem.acquire()就不卡主了。

class UrlProducer(threading.Thread):

    def __init__(self, sem):
        super().__init__()
        self.sem = sem

    def run(self):
        for i in range(20):
            self.sem.acquire() # 没调用一次，semaphore设定的数量减一, 当为0的时候，就卡住
            html_spider = HtmlSpider(self.sem)
            html_spider.start()

if __name__ == '__main__':
    sem = threading.Semaphore(3)
    url_producer = UrlProducer(sem)
    url_producer.start()

# ----------------------------------------------------------------------------------------------------------------------
# 线程池

import time
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed, wait

def get_html(times):
    time.sleep(times)
    print (" got page {} success".format(times))
    return times

# ---------
executor = ThreadPoolExecutor(max_workers=2 )
# 通过submit函数提交执行的函数到线程池中，submit是立即返回
task1 = executor.submit(get_html, (3))
task2 = executor.submit(get_html, (2))
# DONE 用于判断某个任务是否完成
print (task1.done())    # 非阻塞
print (task1.result())  # 阻塞
print (task2.cancel())  # 关闭 - 无非取消执行中和执行完成的

# ------
# 获取已经成功的task的返回
urls = [3, 2, 4]
all_task = [executor.submit(get_html, (url)) for url in urls]
wait(all_task) # 阻塞,等所有的线程执行完成之后，才继续
print ('main')
for future in as_completed(all_task):
    data = future.result()
    print (data)
# --------
# 通过executor获取已经完成的task
for data in executor.map(get_html, urls):
    print (data)

'''这个与上面那个不同点在于，下面的是根据urls的顺序做返回值的，上面的as_completed是根据谁先执行完成，谁先返回的'''
# ----------------------------------------------------------------------------------------------------------------------

from concurrent.futures import Future
# 未来对象，task的返回容器

from multiprocessing import Process