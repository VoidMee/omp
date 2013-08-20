import cv2
import numpy as np
import wx

from lib.grabber import Grabber
from cfg.constants import *

class SampleCapturer(object):
    def __init__(self, parent):
        self.parent = parent        


        try:
            self._checkDevice()
            self.selection = []
        except IOError:
            raise Exception("No Capturing Device Found. Please make sure the hardward is properly connected or drivers are missing.")
        else:
            self.frameName = "Capturer"
            self.window = cv2.namedWindow(self.frameName, cv2.CV_WINDOW_AUTOSIZE)
            cv2.setMouseCallback("Capturer", self.on_mouse)
            self.drag_start = None      # Set to (x,y) when mouse starts drag
            self.track_window = None    # Set to rect when the mouse drag finishes

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

    def run(self):
        global FILEINDEX
        while self.frame != None:
            cv2.imshow(self.frameName, self.frame)
            c = cv2.waitKey(1)
            if c == 27:
                cv2.destroyWindow(self.frameName)
                break
            elif c == ord('s'):
                cv2.imwrite("D:\grs_data\grs_" + str(FILEINDEX) + ".jpg", self.frame[self.selection[1]+1:self.selection[3]-1, self.selection[0]+1:self.selection[2]-1])
                FILEINDEX += 1
                
            self.frame = self.capture.read()[1]
            if self.drag_start or self.track_window:
                cv2.rectangle(self.frame, (self.selection[0], self.selection[1]), (self.selection[2], self.selection[3]), (0, 200, 0), 1)


    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drag_start = (x, y)
        if event == cv2.EVENT_LBUTTONUP:
            self.drag_start = None
            self.track_window = self.selection
        if self.drag_start:
            xmin = min(x, self.drag_start[0])
            ymin = min(y, self.drag_start[1])
            xmax = max(x, self.drag_start[0])
            ymax = max(y, self.drag_start[1])
            self.selection = (xmin, ymin, xmax, ymax)
            