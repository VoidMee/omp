import win32api as wa

from abc import ABCMeta, abstractmethod

class Handler(object):
    __metaclass__ = ABCMeta

class MouseHandler(Handler):
    
    def __init__(self):

        dict = wa.GetMonitorInfo(1) #argument 1 for standard input Monitor
        _, _, self.xmax, self.ymax = dict['Monitor']