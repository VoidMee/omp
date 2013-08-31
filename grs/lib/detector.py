import cv2

from abc import ABCMeta, abstractmethod

class Detector(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def detect(self, frame):
        pass

class BProjectionDetector(Detector):
    
    def __init__(self, hist):
        self.hist = hist

    def detect(self, frame):
        return cv2.calcBackProject([frame], [0, 1], self.hist, ranges=[0, 180, 0, 255], scale=1.0)