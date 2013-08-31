import win32api as wa

from abc import ABCMeta, abstractmethod

from cfg.constants import *
from lib.util import *

class Handler(object):
    __metaclass__ = ABCMeta

class MouseHandler(Handler):
    
    def __init__(self):

        dict = wa.GetMonitorInfo(1) #argument 1 for standard input Monitor
        _, _, self.xmax, self.ymax = dict['Monitor']
        
        self.fx, self.fy = FRAMESIZE

        self.thresh_dist = 10

        self.l = LinkedList()

        self.l.push((120, 120, 80, 80))
        self.l.push((120, 120, 80, 80))
        self.l.push((120, 120, 80, 80))
        self.l.push((120, 120, 80, 80))

        self.pointTrace = LinkedList()
        self.pointTrace.push(1)
        self.pointTrace.push(1)
        self.pointTrace.push(1)
        self.pointTrace.push(1)

    def handle(self, (x, y, w, h), posture):

        flag = self.evaluateEvent(posture)

        if flag:
            print posture

        self.pointTrace.push(posture)
        
        pcx, pcy = self.getMidpoints(self.l.topElement())
        mx, my = self.getMidpoints((x, y, w, h))

        if abs(mx -pcx) < self.thresh_dist and abs(my - pcy) < self.thresh_dist:
            #xpos = int(mx * self.xmax / self.fx)
            #ypos = int(my * self.ymax / self.fy)
            pcx = int(2.5 * (pcx - 60))
            pcy = int(2.5 * (pcy - 60))
            wa.SetCursorPos((pcx, pcy))
        else:
           mx = int(2.5 * (mx - 60))
           my = int(2.5 * (my - 60))
           wa.SetCursorPos((mx, my))
           #pcx = int(pcx * self.xmax / self.fx)
           #pcy = int(pcy * self.ymax / self.fy)
           wa.SetCursorPos((mx, my))

        self.l.push((x, y, w, h))
        self.l.pop()

    def evaluateEvent(self, posture):
        temp = self.pointTrace.elements()
        flag = True
        for item in temp:
            if item != posture:
                flag = False
                break
        return flag
        pass

    def getMidpoints(self, (x, y, w, h)):
        return int(x + w / 2.0), int(y + h / 2.0)