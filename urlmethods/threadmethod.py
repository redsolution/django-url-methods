"""
Decorator ``threadmethod`` makes method always executable
in separated new thread with a specified timeout,
propagating exceptions and result. 

>>> from threadmethod import threadmethod
>>> from time import sleep

>>> @threadmethod()
>>> def separate():
>>>     return 'Done.'
>>> separate()
'Done.'

>>> @threadmethod(2.0)
>>> def connect(host):
>>>     sleep(5)
>>>     return host
>>> connect('example.com')
Traceback (most recent call last):
    ...
threadmethod.ThreadTimeoutException

>>> @threadmethod(return_immediately=True)
>>> def immediately(host):
>>>     sleep(3)
>>>     return host
>>> thread = immediately('example.com')
>>> thread.join()
>>> thread.result
'example.com'
"""

from threading import Thread

class ThreadTimeoutException(Exception):
    pass

class ThreadMethodClass(Thread):
    def __init__(self, target, args, kwargs):
        super(ThreadMethodClass, self).__init__()
        self.target, self.args, self.kwargs = target, args, kwargs
    
    def run(self):
        self.result = None
        self.exception = None
        try:
            self.result = self.target(*self.args, **self.kwargs)
        except BaseException, exception:
            self.exception = exception

def threadmethod(timeout=None, return_immediately=False):
    def wrapper(func):
        def runner(*args, **kwargs):
            thread = ThreadMethodClass(target=func, args=args, kwargs=kwargs)
            thread.start()
            if return_immediately:
                return thread
            thread.join(timeout)
            if thread.isAlive():
                raise ThreadTimeoutException
            elif thread.exception is not None:
                raise thread.exception
            return thread.result
        runner.__name__ = getattr(func, '__name__', 'unknown')
        return runner
    return wrapper
