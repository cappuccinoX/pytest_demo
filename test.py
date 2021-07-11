def triangles():
     L = [1]
     while True:
        yield L
        L = [1] + [L[i] + L[i + 1] for i in range(len(L) - 1)] + [1]

    # 第二种写法
    # L = [1]
    # while True:
    #     yield L[:len(L)]
    #     L.append(0)
    #     L = [L[x - 1] + L[x] for x in range(len(L))]

#利用map()函数，把用户输入的不规范的英文名字，变为首字母大写，其他小写的规范名字。输入：['adam', 'LISA', 'barT']，输出：['Adam', 'Lisa', 'Bart']
def normalize(name):
    return name[0].upper() + name[1:].lower()

def test_triangles():
    n = 0
    results = []
    for t in triangles():
        results.append(t)
        n = n + 1
        if n == 10:
            break

    for t in results:
        print(t)

    if results == [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1],
        [1, 5, 10, 10, 5, 1],
        [1, 6, 15, 20, 15, 6, 1],
        [1, 7, 21, 35, 35, 21, 7, 1],
        [1, 8, 28, 56, 70, 56, 28, 8, 1],
        [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
    ]:
        print('测试通过!')
    else:
        print('测试失败!')


from multiprocessing import Process, Pool, Queue, Pipe
from multiprocessing.managers import BaseManager
import os, time, random, threading
import queue

def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

def test_process():
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')

def long_time_task(name):
    print("Current parent process %s" % os.getppid())
    print("Run task %s (%s)..." % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print("Task %s runs %0.2f seconds." % (name, (end - start)))

def test_pool():
    print("Parent process %s." % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print("Waiting for all subprocesses done...")
    p.close()
    p.join()
    print('All subprocesses done.')

def write(q):
    print("Process to write: %s" % os.getpid())
    for value in ["A", "B", "C"]:
        print("Put value %s to queue..." % value)
        q.put(value)
        time.sleep(random.random() * 3)

def read(q):
    print("Process to read: %s" % os.getpid())
    while True:
        value = q.get(True)
        print("Get %s from queue." % value)

def test_communication_between_processes():
    # 父进程创建Queue，并传给各个子进程
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入:
    pw.start()
    # 启动子进程pr，读取:
    pr.start()
    # 等待pw结束:
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()


def loop():
    print("thread %s is running..." % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print("thread %s >>> %s" % (threading.current_thread().name, n))
        time.sleep(1)
    print("thread %s ended." % threading.current_thread().name)

def test_thread():
    print('thread %s is running...' % threading.current_thread().name)
    t = threading.Thread(target=loop, name="LoopThread")
    t.start()
    t.join()
    print('thread %s ended.' % threading.current_thread().name)

balance = 0
def test_thread_1():
    lock = threading.Lock()
    def change_it(n):
        global balance
        balance = balance + n
        balance = balance - n
    def run_thread(n):
        for i in range(2000000):
            # 获取锁
            lock.acquire()
            try:
                change_it(n)
            finally:
                lock.release()
    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance)

def test_local_thread():
    # 创建全局ThreadLocal对象
    local_school = threading.local()

    def process_student():
        # 获取当前线程关联的student
        std = local_school.student
        print("Hello, %s (in %s)" % (std, threading.current_thread().name))
    
    def process_thread(name):
        # 绑定ThreadLocal的student
        local_school.student = name
        process_student()
    
        t1 = threading.Thread(target=process_thread, args=("Alice",), name="Thread-A")
        t2 = threading.Thread(target=process_thread, args=("Bob",), name="Thread-B")
        t1.start()
        t2.start()
        t1.join()
        t2.join()


if __name__ == "__main__":
    pass