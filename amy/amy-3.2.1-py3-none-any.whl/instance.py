from threading import Thread


def passFunc(self, *args, **kwargs): pass

def initSuper(self, cls, *args, **kwargs): cls.__init__(self, *args, **kwargs)

def passDefault(cls, name, func=passFunc):
    if not hasattr(cls, name):
        setattr(cls, name, func)

def startThead(self, function):
    self.__thread = Thread(target=function)
    self.__thread.start()


def stopThread(self):
    if hasattr(self, '__thread'):
        self.__thread.join()


def instance(cls):

    setattr(cls, '__init__', passFunc)

    passDefault(cls, 'onCreate')
    passDefault(cls, 'onAuth')
    passDefault(cls, 'isAuthorized')
    passDefault(cls, 'onStart')
    passDefault(cls, 'onStop')
    passDefault(cls, 'sendMessage')
    passDefault(cls, 'onDelete')
    passDefault(cls, 'startThead', startThead)
    passDefault(cls, 'stopThread', stopThread)

    return cls


@instance
class Instance:
    pass
