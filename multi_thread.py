
import threading
import time
import random
import queue

gMoney = 0
gLock = threading.Lock()
gCondiction = threading.Condition()
q = queue.Queue(4)

class Producer(threading.Thread):
    def run(self):
        global gMoney
        global gLock
        while True:
            # gLock.acquire()
            # gCondiction.acquire()
            money = random.randint(10,100)
            gMoney += money
            q.put(gMoney)   # 队列存
            print('Producer %s conduct money %d, balance is %d'%(threading.current_thread(),money, gMoney))
            # gLock.release()
            # gCondiction.notify_all()
            # gCondiction.release()
            time.sleep(1)


class Consumer(threading.Thread):
    def run(self):
        # global gMoney
        global gLock
        while True:
            # gLock.acquire()
            # gCondiction.acquire()
            money = random.randint(10, 100)
            # while gMoney >= money:
            #     if gMoney >= money:
            #         gMoney -= money
            #         print('Consumer %s spent money %d, balance is %d' % (threading.current_thread(), money, gMoney))
            # else:
            #     print('balance is not enough')
            #     gCondiction.wait()
            # while gMoney < money:
                # print('balance is not enough')
                # gCondiction.wait()
            gMoney = q.get()    # 队列取
            gMoney -= money
            print('Consumer %s spent money %d, balance is %d' % (threading.current_thread(), money, gMoney))
            # gLock.release()
            # gCondiction.release()
            time.sleep(1)

def main():
    for i in range(1):
        p = Producer(name='Producer %s'%i)
        p.start()

    for i in range(1):
        c = Consumer(name='Consumer %s'%i)
        c.start()

class Tester(threading.Thread):
    def __init__(self,index):
        threading.Thread.__init__(self)
        self.index = index

    def run(self):
        print("I'm thread {}".format(self.index))
        time.sleep(self.index)
        print("Thread {} end".format(self.index))

def func1(index):
    print("I'm thread {}".format(index))
    time.sleep(index)
    print("Thread {} end".format(index))

if __name__ == '__main__':
        # main()
        start_time = time.time()
        thread_list = []
        # 实例化一个线程
        # target是目标函数，记得别加括号
        # args是目标函数的参数，当参数个数仅有一个时，记得后面加上','逗号
        for index in range(1, 10):
            # thread_list.append(threading.Thread(target=func1, args=(index,)))
            thread_list.append(Tester(index))
        # 用start启动线程
        for t in thread_list:
            t.start()
        # join表示等待线程执行结束
        for t in thread_list:
            t.join()
        print("用时：{:.2f}s".format(time.time() - start_time))