class EmptyQueueException(Exception):
    def __init__(self):
        super.__init__("Queue is empty!")


class FullQueueException(Exception):
    def __init__(self):
        super.__init__("Queue is full!")


class Queue():
    def __init__(self, size = 40):
        self._array = [None for i in range(40)]
        self._size = size
        self._beginIndex = 0
        self._endIndex = 0

    def isEmpty(self):
        return self._beginIndex == self._endIndex

    def isFull(self):
        return self._beginIndex == (self._endIndex + 1) % self._size

    def dequeue(self):
        try:
            if self.isEmpty():
                raise EmptyQueueException()
            retValue = self._array[self._beginIndex]
            self._beginIndex += 1
            self._beginIndex %= self._size

            return retValue

        except EmptyQueueException:
            return None

    def enqueue(self, elem):
        try:
            if self.isFull():
                raise FullQueueException()
            self._array[self._endIndex] = elem
            self._endIndex += 1
            self._endIndex %= self._size

        except FullQueueException:
            return None

    def __sizeof__(self):
        return self._size

    def first(self):
        try:
            if self.isEmpty():
                raise EmptyQueueException()

            return self._array[self._beginIndex]

        except EmptyQueueException:
            return None

    def clear(self):
        self._array = [None for i in range(40)]
        self._beginIndex = 0
        self._endIndex = 0

    def peakQueue(self):
        return self._array