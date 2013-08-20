import cv2
import numpy as np
import threading
import wx

from cfg.constants import PROJECTDIR
from cfg.constants import DATAPATHNAME
from cfg.constants import CLASSIFIERDIRNAME
from cfg.constants import NNTRAINERFILENAME

class NNTrainer(threading.Thread):
    
    def __init__(self, parent, trainingFilepaths):
        threading.Thread.__init__(self)
        #
        # Create an Artificial Neural Network with
        # No.of Hidden Layers = 2
        # [128, 128, 128, 4]
        #
        self.nn = cv2.ANN_MLP(np.array([128, 128, 128, 4]), cv2.ANN_MLP_SIGMOID_SYM)
        
        # Load Previouly trained data
        self.nn.load(DATAPATHNAME + CLASSIFIERDIRNAME + NNTRAINERFILENAME)
        
        self.trainingDatas =[]
        self.detector = cv2.SURF(400, 5, 5)

        self.parent = parent
        self.trainingFilepaths = trainingFilepaths

        self.setDaemon(True)
        
        wx.CallAfter(self.parent.logMessage, "Trainer class 'NNTrainer' initialized\n")
    def run(self):
        wx.CallAfter(self.parent.logMessage, "Training Started *** \n")

        # Terminate if no training files supplied
        if self.trainingFilepaths == None or len(self.trainingFilepaths) < 1:
            wx.CallAfter(self.parent.logMessage, "No Training Data Supplied. Now terminating ... \n")
            return False

        ########################
        # Prepare Training Datas
        wx.CallAfter(self.parent.logMessage, "Preparing Data ... \n")
        paths = []
        for trainingCols in self.trainingFilepaths:
            path = trainingCols[0]
            for filename in trainingCols[1]:
                fullpath = path + "\\" + filename
                paths.append(fullpath)
        flag = True
        for idx, file in enumerate(paths):
            img = cv2.imread(file)
            if img == None:
                flag = False
                fidx = idx
                break
            wx.CallAfter(self.parent.logMessage, "Extracting features of " + file + " ...\n")
            k, d = self.detector.detectAndCompute(img, None)
            m, e = cv2.PCACompute(d)
            self.trainingDatas.append(m[0])

        wx.CallAfter(self.parent.logMessage, "Features extracted\n")
        if flag == True:
            wx.CallAfter(self.parent.logMessage, "Training Datas prepared successfully\n")
        else:
            wx.CallAfter(self.parent.logMessage, "Error while preparing training datas \n")
            return False

        # Training datas Prepared
        ##########################

        ############################
        # Beginning the training Phase
        wx.CallAfter(self.parent.logMessage, "Running the training phase ...\n")

        outputValues = [[1.0, 0., 0., 0.]] * len(self.trainingDatas)

        self.nn.train(np.array(self.trainingDatas), np.array(outputValues), None)
        #print(DATAPATHNAME + CLASSIFIERDIRNAME + NNTRAINERFILENAME)
        self.nn.save(PROJECTDIR + DATAPATHNAME + CLASSIFIERDIRNAME + NNTRAINERFILENAME)
        wx.CallAfter(self.parent.logMessage, "Classifier trained successfully\n")
        self.parent.trainButton.Enable()
        # Training finished
        ############################

    def _trainNetwork(self):
        if self.trainingFilepaths == None or len(self.trainingFilepaths) < 1:
            return "No Datas Provided"

        ############################################################################
        # Prepare Training Datas
        self.parent.sysEventLabel.SetLabel("Preparing data ...")

        retVal, arg = self._prepareTrainingDatas()
        self.parent.sysEventLabel.SetLabel("Training Data prepared")

        return arg


    def _prepareTrainingDatas(self):

        paths = []
        for trainingCols in self.trainingFilepaths:
            path = trainingCols[0]
            for filename in trainingCols[1]:
                fullpath = path + "\\" + filename
                paths.append(fullpath)
        flag = True
        surf  = cv2.SURF(400, 5, 5)
        for idx, file in enumerate(paths):
            img = cv2.imread(file)
            if img == None:
                flag = False
                fidx = idx
                break
            print idx
            k, d = surf.detectAndCompute(img, None)
            m, e = cv2.PCACompute(d)
            self.trainingDatas.append(m[0])
        if flag == True:
            return True, "Prepared Training Datas"
        else:
            return False, "No Image file named " + paths[fidx]
__all__ = ["NNTrainer"]