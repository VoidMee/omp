import cv2
import numpy as np

from cfg.constants import DATAPATHNAME
from cfg.constants import NNTRAINERFILENAME

class NNTrainer(object):
    
    def __init__(self):
        #
        # Create an Artificial Neural Network with
        # No.of Hidden Layers = 2
        # [128, 128, 128, 4]
        #
        self.nn = cv2.ANN_MLP(np.array([128, 128, 128, 4]), cv2.ANN_MLP_SIGMOID_SYM)

        # Load Previouly trained data
        self.nn.load(DATAPATHNAME + NNTRAINERFILENAME)
        pass

    def trainNetwork(self, trainingDatas=None):
        if trainingDatas == None or len(trainingDatas) < 1:
            return "No Datas Provided"
        return len(trainingDatas)

__all__ = ["NNTrainer"]