import cv2

from abc import ABCMeta, abstractmethod

class Tracker(object):
    __metaclass = ABCMeta

    def track(self, frame, prevWindow):
        pass

class CamShiftTracker(Tracker):

    def __init__(self, criteria):
        self.crit = criteria

    def track(self, frame, prevWindow):
        return cv2.CamShift(frame, prevWindow, self.crit)