
class Stack:
    def __init__(self, arr = None):
        """
        Constructor for stack class.

        Parameters
        ----------
        arr
           list
           an optional array to start with 
        """
        if arr is None:
            self.stack = []
            self.count = 0
        elif not isinstance(arr,list):
            raise TypeError('arr must be of type list')
        else:
            self.stack = arr
            self.count = len(arr)
    def push(self,elem):
        """push element to stack"""
        self.stack.append(elem)
        self.count += 1
    def pop(self):
        """pop element from stack"""
        if self.isEmpty():
            raise IndexError('pop from empty stack')
        self.count -= 1
        return self.stack.pop()
    def peek(self):
        """return the next element without popping"""
        if self.isEmpty():
            return None
        else:
            return self.stack[-1]
    def get_list(self):
        """return stack's list"""
        return self.stack
    def isEmpty(self):
        """check if stack is empty"""
        if self.count == 0:
            return True
        return False
class Queue:
    def __init__(self,arr = None):
        """
        Constructor for Queue class

        Parameters
        ----------
        arr
        list 
        an optional array to start with 
        """
        if arr is None:
            self.queue = []
            self.count = 0
        elif not isinstance(arr,list):
            raise TypeError('arr must be of type list')
        else:
            self.queue = arr
            self.count = len(arr)
    def enqueue(self,elem):
        """enqueue element to queue"""
        self.queue.append(elem)
        self.count += 1 
    def dequeue(self):
        """dequeue element from queue"""
        if self.isEmpty():
            raise IndexError('dequeue from empty queue')
        if self.count == 1:
            self.count -= 1
            return self.queue.pop()
        elem = self.queue[0]
        for i in range(1,self.count):
            self.queue[i-1] = self.queue[i]
        self.count -= 1
        self.queue.pop()
        return elem
    def peek(self):
        """return next element without dequeing"""
        if self.isEmpty():
            return None
        return self.queue[0]
    def get_list(self):
        """return queue's list"""
        return self.queue
    def isEmpty(self):
        """check if queue is empty"""
        if self.count == 0:
            return True
        return False

    