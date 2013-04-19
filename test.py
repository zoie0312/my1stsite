import time
from multiprocessing import Process

def start_time():
    start = time.time()
    print "update timer = %r" % start
    while (time.time() - start) < 30:
        pass

    print "Time's Up!"
    print "Now, it is %r" % time.time()

#def start():
#    start_time()
#    return

#if __name__ == '__main__':
p = Process(target=start_time)
p.start()
for i in range(0, 32):
     time.sleep(1)
     print "QQQ"
    #p.join()
