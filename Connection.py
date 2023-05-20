import struct
import socket
import time
import utils
from threading import Thread
from CycleBuffer import CycleBuffer


def asShortArray(buff):
    res = []

    for i in range(len(buff) // 2):
        res.append(struct.unpack_from('h', buff, i * 2)[0])
    return res


class Connection(Thread):
    def __init__(self, cb):
        Thread.__init__(self)
        self.daemon = True
        self.cb = cb
        self.UDP_IP = "127.0.0.1"
        self.UDP_PORT = 5555
        self.SIZE = 1392
        self.channel = [0, 1, 2, 3, 4, 5, 6, 7]
        self.union_data = []
        self.channel_total = 29
        self.dimension = 24
        self.mode = 0
        self.size_of_data = 1200
        self.prev_mean = None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))

        self.val = CycleBuffer(200)
        self.timer = CycleBuffer(5)

    def setChannel(self, c):
        self.channel = c

    def setAvgSize(self, size):
        self.val.setSize(size)

    def setMode(self, m):
        self.mode = m

    def run(self):
        prevTime = time.time()
        prevVal = 0

        while True:
            data, addr = self.sock.recvfrom(self.SIZE)
            curr = time.time()
            self.timer.add(curr - prevTime)
            prevTime = curr

            arr = asShortArray(data)
            test = []
            for i in range(len(self.channel)):
                test.append(arr[self.channel[i] * self.dimension:self.channel[i] * self.dimension + 24])

            if len(self.union_data) == 0:
                self.union_data = test
                continue
            if len(self.union_data[0]) < self.size_of_data:
                for i in range(len(self.union_data)):
                    self.union_data[i] += test[i]
            else:
                if self.prev_mean is None:
                    self.prev_mean = utils.find_min_ampl(self.union_data)
                else:
                    if utils.is_depr(utils.find_min_ampl(self.union_data), self.prev_mean):
                        print("depression")
                        self.cb(0, True)
                    else:
                        self.cb(0, False)
                    self.prev_mean = utils.find_min_ampl(self.union_data)
                self.union_data.clear()

            # for i in range(self.dimension):
            #     val = arr[self.channel[0] * self.dimension + i]
            #     s += val
            #     if self.mode == 0:
            #         self.val.add(abs(val))
            #     elif self.mode == 1:
            #         self.val.add(max(prevVal, val) - min(prevVal, val))
            #     else:
            #         self.val.add(val)
            #
            #     prevVal = val
            #
            # self.cb(0 if self.timer.getAvg() < 1e-7 else 1 / self.timer.getAvg(),
            #         self.val.getAvg() if self.mode in [0, 1] else abs(self.val.getAvg() - s / 24))