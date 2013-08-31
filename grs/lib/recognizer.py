from abc import ABCMeta, abstractmethod

from cfg.constants import *

import cv2
import numpy as np

class Recognizer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def recognize(self, frame):
        pass

class HandRecognizer(Recognizer):

    def __init__(self):
        #initialize the boost tree
        self._boost = cv2.GBTrees()
        self._boost.load(PROJECTDIR + DATAPATHNAME + MODELNAME)
        
        #initializef feature extractor
        self._featureExtractor = cv2.SURF(400, 4, nOctaveLayers=4, extended=False)
        #self._es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
        pass

    def recognize(self, frame, (x, y, w, h)):
        hand = frame[y:y+h, x:x+w]
        k, d = self._featureExtractor.detectAndCompute(hand, None)
        if d != None:
            m, e = cv2.PCACompute(d)
            
            for idxs in range(len(m)):
                for idx in range(len(m[idxs])):
                    m[idxs][idx] = int(m[idxs][idx] * 1000)

            temp = np.array(m, dtype=np.float32)
            sample_n, var_n = temp.shape
            samples = np.zeros((sample_n * 3, var_n +1), np.float32)
            samples[:, :-1] = np.repeat(temp, 3, axis=0)
            samples[:, -1] = np.tile(np.arange(3), sample_n)
        
            pred = np.array([self._boost.predict(s) for s in samples])
            pred = pred.reshape(-1, 3).argmax(1)
        else: pred = 0
        return pred