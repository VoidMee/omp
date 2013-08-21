import cv2
import numpy as np

from cfg.constants import MAXCAMERAINDEX

class FrameGrabber():
    
    def __init__(self):
        try:
            self._checkDevice()
        except IOError:
            raise IOError("No Capturing Device Found. Please make sure the hardward is properly connected or drivers are missing.")
            

    def _checkDevice(self):
        self.currentCameraIndex = 0
        self.capture = cv2.VideoCapture(self.currentCameraIndex)
        self.frame = self.capture.read()[1]
        while self.frame == None:
            self.currentCameraIndex += 1
            if self.currentCameraIndex > MAXCAMERAINDEX:
                break
            self.capture = cv2.VideoCapture(self.currentCameraIndex)
            _, self.frame = self.capture.read()
        if self.frame == None:
            raise IOError
    def grabNext(self):
        self.frame = self.capture.read()[1]
        if self.frame != None:
            return self.frame
        else:
            raise IOError("No Capturing Device found. Please make sure the hardward is properly connected or drivers are missing.")
    """
    def run(self):
        self.frameName = "GRS"
        self.window = cv2.namedWindow(self.frameName, cv2.CV_WINDOW_AUTOSIZE)
        while self.frame != None:
            cv2.imshow(self.frameName, self.frame)
            c = cv2.waitKey(1)
            if c == 27:
                cv2.destroyWindow(self.frameName)
                break
            self.frame = self.capture.read()[1]

    def __del__(self):
        cv2.destroyWindow(self.frameName)
        print "Grabber deleted"
    """
__all__ = ["FrameGrabber"]