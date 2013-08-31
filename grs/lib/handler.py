import win32api as wa
import win32con as wc

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

        self.thresh_dist = 20

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

        self.state = 1

    def handle(self, (x, y, w, h), posture):

        #flag = self.evaluateEvent(posture)


        #self.pointTrace.push(posture)
        
        pcx, pcy = self.getMidpoints(self.l.topElement())
        mx, my = self.getMidpoints((x, y, w, h))

        if abs(mx -pcx) < self.thresh_dist and abs(my - pcy) < self.thresh_dist:
            print "inside threshold posture", posture
            #apply gesture and do not change cursor position
            #xpos = int(mx * self.xmax / self.fx)
            #ypos = int(my * self.ymax / self.fy)
            #pcx = int(2.5 * (pcx - 60))
            #pcy = int(2.5 * (pcy - 60))
            #wa.SetCursorPos((pcx, pcy))
    
            if self.state == 1 and posture == 0:

                #print "click"
                wa.mouse_event(wc.MOUSEEVENTF_LEFTDOWN, pcx, pcy)
                self.state = 0
            elif self.state == 0 and posture == 1:
                #print "pointer"
                wa.mouse_event(wc.MOUSEEVENTF_LEFTUP, pcx, pcy)
                self.state = 1
            elif self.state == 0 and posture == 2:
                pass
        else:
           print "outside threshold"
           #move cursor and do not apply gesture
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