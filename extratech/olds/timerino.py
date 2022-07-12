import threading
import time

class Timer(threading.Thread):
    def __init__(self, count, colbecca, *args):
        threading.Thread.__init__(self)
        self.arghi = args
        self.event = threading.Event()
        self.count = count
        self.colbecca = colbecca

    def run(self):
        while self.count > 0 and not self.event.is_set():
            print (self.count)
            self.count -= 1
            self.event.wait(1)
        if self.count == 0:
            if self.arghi:
                self.colbecca(self.arghi)
                # print('gli arghi')
                print(self.arghi)
            else:
                self.colbecca()

    def stop(self):
        self.event.set()

# def porcoMondo():
#     print('porcomondo')

# tmr = Timer(5, porcoMondo)
# tmr.start()

# time.sleep(3)
# print('ti stoppo')

# tmr.stop()