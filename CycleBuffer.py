import queue


class CycleBuffer:
    def __init__(self, size):
        self.size = size
        self.sum = 0
        self.count = 0
        self.q = queue.Queue()

    def setSize(self, size):
        while self.size > size:
            self.size -= 1
            self.q.get()

    def clear(self):
        self.sum = 0
        self.count = 0
        self.q = queue.Queue()

    def add(self, val):
        self.sum += val
        self.q.put(val)
        self.count += 1
        if self.count > self.size:
            self.sum -= self.q.get()
            self.count -= 1

    def getAvg(self):
        if self.count == 0:
            return None
        return self.sum / self.count