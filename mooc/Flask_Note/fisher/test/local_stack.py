# -*- coding:utf-8 -*-
import threading, time
from werkzeug.local import LocalStack

my_stack = LocalStack()
my_stack.push(1)


def worker():
    # 新线程
    # 第一个打印的是什么，打印的是none，为什么，因为主线程推入了1，但是子线程没有推入，所以这里拿到的东西是空的
    print('in new thread before push, value is: ' + str(my_stack.top))
    my_stack.push(2)
    print('in new thread after push, value is: ' + str(my_stack.top))


new_t = threading.Thread(target=worker, name='shine_thread')
new_t.start()
time.sleep(1)
# 主线程
print('finally, in main thread value is ' + str(my_stack.top))


'''

1. 以线程ID号作为key的字典 -> Local -> LocalStack

2. AppContext RequestContext -> LocalStack

3. Flask -> AppContext  Request -> RequestContext

4. current_app -> (LocalStack.top = AppContext top.app = Flask)

5. request -> (LocalStack.top = RequestContext top.request = Request)

'''