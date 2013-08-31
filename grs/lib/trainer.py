import cv2
import numpy as np
import threading
import wx
import os

class NNTrainer(threading.Thread):
    
    def __init__(self, parent, trainingFilepaths):
        threading.Thread.__init__(self)
        #
        # Create an Artificial Neural Network with
        # No.of Hidden Layers = 2
        # [128, 128, 128, 4]
        #
        self.nn = cv2.ANN_MLP(np.array([128, 128, 128, 3]), cv2.ANN_MLP_SIGMOID_SYM)
        
        # Load Previouly trained data
        self.nn.load(PROJECTDIR + DATAPATHNAME + CLASSIFIERDIRNAME + NNTRAINERFILENAME)
        
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
            if d != None:
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

        selection = self.parent.outputOptionRadio.GetStringSelection()
        output = OUTPUTLISTS[selection]

        wx.CallAfter(self.parent.logMessage, "** for " + selection + " with output: " + str(output) + "\n")
        outputValues = [output] * len(self.trainingDatas)

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

class BTrainer(object):
    def __init__(self):
        self.boost = cv2.Boost()
        self.surf = cv2.SURF(400, 4, nOctaveLayers=4, extended=False)

    def train(self):
        samples = []

        #for fist
        print "collecting samples for fist"
        fist_files = os.listdir("D:/workspace/python/omp/grs/data/trainings/fist")
        for files in fist_files:
            src = cv2.imread("D:/workspace/python/omp/grs/data/trainings/fist/" + files)
            print files
            k, d = self.surf.detectAndCompute(src, None)
            if d != None:
                m, e = cv2.PCACompute(d)
                samples.append(m[0])
        
        #for open
        print "collecting samples for open"
        open_files = os.listdir("D:/workspace/python/omp/grs/data/trainings/open")
        for files in open_files:
            src = cv2.imread("D:/workspace/python/omp/grs/data/trainings/open/" + files)
            print files
            k, d = self.surf.detectAndCompute(src, None)
            if d != None:
                m, e = cv2.PCACompute(d)
                samples.append(m[0])
        """
        #for negative
        print "collecting samples for negative"
        negatives = os.listdir("D:/workspace/python/omp/grs/data/trainings/NegativeImages")
        for files in negatives:
            src = cv2.imread("D:/workspace/python/omp/grs/data/trainings/NegativeImages/" + files)
            print files
            k, d = self.surf.detectAndCompute(src, None)
            if d != None:
                m, e = cv2.PCACompute(d)
                samples.append(m[0])
        print "finished collecting samples"
        """
        samples = np.array(samples, dtype=np.float32)
    
        sample_n, var_n = samples.shape
        new_samples = np.zeros((sample_n * 3, var_n +1), np.float32)
        new_samples[:, :-1] = np.repeat(samples, 3, axis=0)
        new_samples[:, -1] = np.tile(np.arange(3), sample_n)

        
        responses = [1, 0, 0] * len(fist_files)
        responses += [0, 1, 0] * len(open_files)
        #responses += [0, 0, 1] * len(negatives)

        print len(new_samples)
        print len(responses)

        new_responses = np.array(responses, dtype=np.int32)

        var_types = np.array([cv2.CV_VAR_NUMERICAL] * var_n + [cv2.CV_VAR_CATEGORICAL, cv2.CV_VAR_CATEGORICAL], np.uint8)
    
        
        ret = self.boost.train(new_samples, cv2.CV_ROW_SAMPLE, new_responses, varType=var_types, params=dict(max_depth=5))
        print ret
        self.boost.save("D:/model.xml")
        self.boost.load("D:/model.xml")
        pass

class BoostTrainer(threading.Thread):
    """
    Training with the boosting method.
    boost_type : Real AdaBoost
    """

    def __init__(self, parent, trainingFilepaths):
        threading.Thread.__init__(self)
        self.parent = parent
        self.setDaemon(True)
        self.trainingDatas =[]
        self.trainingFilepaths = trainingFilepaths

        self._model = cv2.Boost()
        self._class_n = OUTPUTCLASSCOUNTS
        self._tflag = cv2.CV_ROW_SAMPLE
        self._params = dict(max_depth=5)

        self.detector = cv2.SURF(400, 4, nOctaveLayers=4, extended=False)

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
            if d != None:
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

        selection = self.parent.outputOptionRadio.GetStringSelection()
        output = OUTPUTLISTS[selection]

        wx.CallAfter(self.parent.logMessage, "** for " + selection + " with output: " + str(output) + "\n")
        outputValues = np.array([output] * len(self.trainingDatas), dtype=np.int32)
        #self._unrollResponses(outputValues)
        self._unrollTrainingDatas()
        outputValues = np.reshape(outputValues,len(self.trainingDatas))

        #print self.trainingDatas
        #print outputValues
        _, var_n =self.trainingDatas.shape
        var_types = np.array([cv2.CV_VAR_NUMERICAL] * (var_n - 1) + [cv2.CV_VAR_CATEGORICAL, cv2.CV_VAR_CATEGORICAL], np.uint8)
        ret = self._model.train(self.trainingDatas, self._tflag, outputValues, varType=var_types, params=self._params)
        print ret
        #self._model.save(PROJECTDIR + DATAPATHNAME + "model.data")
        #self.nn.train(np.array(self.trainingDatas), np.array(outputValues), None)
        #print(DATAPATHNAME + CLASSIFIERDIRNAME + NNTRAINERFILENAME)
        #self.nn.save(PROJECTDIR + DATAPATHNAME + CLASSIFIERDIRNAME + NNTRAINERFILENAME)

        wx.CallAfter(self.parent.logMessage, "Classifier trained successfully\n")
        self.parent.trainButton.Enable()
        # Training finished
        ############################

    def _unrollTrainingDatas(self):
        self.trainingDatas = np.array(self.trainingDatas)
        sample_n, var_n = self.trainingDatas.shape
        new_samples = np.zeros((sample_n * self._class_n, var_n + 1), np.float32)
        new_samples[:, :-1] = np.repeat(self.trainingDatas, self._class_n, axis=0)
        new_samples[:,-1] = np.tile(np.arange(self._class_n), sample_n)
        self.trainingDatas = new_samples

    def _unrollResponses(self, responses):
        print responses
        sample_n = len(responses[0])
        print "sample_n", sample_n
        new_responses = np.zeros(sample_n*self._class_n, np.int32)
        print "new_responses", new_responses
        resp_idx = np.int32( responses + np.arange(sample_n)*self._class_n )
        print "resp_idx", resp_idx
        new_responses[resp_idx] = 1
        print new_responses
        return new_responses

__all__ = ["NNTrainer", "BoostTrainer", "BTrainer"]

if __name__ == "__main__":
    boost = BTrainer()
    boost.train()
