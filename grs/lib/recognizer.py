from abc import ABCMeta, abstractmethod

from cfg.constants import PROJECTDIR
from cfg.constants import TRAINDATAPATH
from cfg.constants import FISTDETECTCLASSIFIER
from cfg.constants import PALMDETECTCLASSIFIER
from cfg.constants import DATAPATHNAME
from cfg.constants import CLASSIFIERDIRNAME

import cv2
import numpy as np

class Recognizer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def recognize(self, frame):
        pass

class HandRecognizer(Recognizer):

    def __init__(self):
        #self._fc = cv2.cv.Load(PROJECTDIR + DATAPATHNAME + CLASSIFIERDIRNAME + "fist.xml")
        #self._pc = cv2.cv.Load(PROJECTDIR + DATAPATHNAME + CLASSIFIERDIRNAME + "palm.xml")
        self._es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
        pass

    def recognize(self, frame):
        #blurring
        self._frame = cv2.medianBlur(frame, 5)

        #grayscale conversion
        #self._frame = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)

        #thresholding
        #_, self._frame = cv2.threshold(self._frame, 100,255, cv2.THRESH_BINARY_INV)

        #erosion
        self._frame = cv2.erode(self._frame, np.ones((3,3), np.uint8))

        #dilation
        self._frame = cv2.dilate(self._frame, self._es)

        return self._frame

        """
        self._fists = cv2.cv.HaarDetectObjects(cv2.cv.fromarray(self._frame), self._fc, cv2.cv.CreateMemStorage())
        self._palms = cv2.cv.HaarDetectObjects(cv2.cv.fromarray(self._frame), self._pc, cv2.cv.CreateMemStorage())

        if len(self._fists) > 0:
            print "Detected fist"
        elif len(self._palms) > 0:
            print "palms"
        else:
            print "Detected None"
        return self._frame
        """