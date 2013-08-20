import wx
import cv2

import numpy as np

from cfg.constants import ROOTFRAMENAME

from lib.grabber import Grabber
from lib.trainer import NNTrainer
from lib.sampler import SampleCapturer

class RootFrame(wx.Frame):

    def __init__(self, parent):
        self.parent = parent
        self.trainingDatas = []
        #self.nnTrainer = NNTrainer(parent=self)

        self._initializeComponents()
        self.trainingThread = None
        self.Show()

    def _initializeComponents(self):
        wx.Frame.__init__(self, None, -1, ROOTFRAMENAME, pos=(10,10), size=(1000, 650), style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)

        #########################################################################################################################
        self.trainPanel = wx.Panel(self, pos=(300, 0), size=(700, 500), style = wx.TAB_TRAVERSAL | wx.BORDER_SIMPLE)

        self.trainButton = wx.Button(self.trainPanel, label="Start Training", pos=(500, 15), size=(150,30))
        self.Bind(wx.EVT_BUTTON, self._onTraining, self.trainButton)

        self.fileUploadLabel = wx.StaticText(parent=self.trainPanel, id=-1, label="Upload Image Data to train:", pos=(50, 70))
        self.fileUploadButton = wx.Button(parent=self.trainPanel, label="Browse", pos=(220, 60), size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self._onOpen, self.fileUploadButton)

        self.settingButton = wx.Button(self.trainPanel, label="Settings", pos=(50,15), size=(60,30))

        outputList = ['fist', 'point', 'open', 'none']
        self.outputOptionRadio = wx.RadioBox(self.trainPanel, -1, "Output", (350, 15), wx.DefaultSize, outputList, 2, wx.RA_HORIZONTAL)

        self.captureButton = wx.Button(parent=self.trainPanel, label="Create Samples", pos=(500, 65), size=(150, 25))
        self.Bind(wx.EVT_BUTTON, self._onCaptureButton, self.captureButton)
        ###########################################################################################################################
        self.testPanel = wx.Panel(self, name="Train Classifier", pos=(0,0), size=(300,500), style = wx.TAB_TRAVERSAL | wx.BORDER_SIMPLE)

        self.testButton = wx.Button(self.testPanel, label="Start Project", pos=(50, 15), size=(160, 30))
        ############################################################################################################################
        self.sysEventPanel = wx.Panel(self, name="System Log", pos=(0, 500), size=(1000, 650), style=wx.TAB_TRAVERSAL|wx.BORDER_SIMPLE)

        self.sysEventLabel = wx.StaticText(parent=self.sysEventPanel, id=-1, label="Output:", pos=(10,5))

        self.outputLog = wx.TextCtrl(parent=self.sysEventPanel, id=-1, value="", pos=(10, 25), style=wx.TE_RICH|wx.TE_MULTILINE, size=(960, 90))




    def _onStartProject(self, event):
        """
        # Start with a numpy array style image I'll call "source"

        # convert the colorspace to RGB from cv2 standard BGR, ensure input is uint8
        img = cv2.cvtColor(np.uint8(source), cv2.cv.CV_BGR2RGB) 

        # get the height and width of the source image for buffer construction
        h, w = img.shape[:2]

        # make a wx style bitmap using the buffer converter
        wxbmp = wx.BitmapFromBuffer(w, h, img)

        # Example of how to use this to set a static bitmap element called "bitmap_1"
        self.bitmap_1.SetBitmap(wxbmp)
        """
        try:
            self.grabber = Grabber()
        except Exception, ex:
            self.sysEventLabel.SetLabel(ex.message)
        else:
            self.Hide()
            self.grabber.run()
            self.Show()
        #"""

    def _onOpen(self, event):
        saveFileDialog = wx.FileDialog(self, "Open Training files", "", "", "JPEG (*.jpg)|*.jpg|Bitmap (*.bmp)|*.bmp|PNG (*.png)|*.png", wx.FD_OPEN | wx.CHANGE_DIR | wx.MULTIPLE)
        retVal = saveFileDialog.ShowModal()
        if retVal == wx.ID_OK:
            fileDirectory = saveFileDialog.GetDirectory()
            fileNames = saveFileDialog.GetFilenames()
            filePaths = [fileDirectory, fileNames]
            self.trainingDatas.append(filePaths) #save file paths for training
            del saveFileDialog
        return

    def _onTraining(self, event):
        self.trainButton.Disable()
        nn = NNTrainer(self, self.trainingDatas)
        self.trainerThread = nn
        nn.start()

    def logMessage(self, msg):
        self.outputLog.AppendText(msg);
        
    def _onCaptureButton(self, event):
        try:
            self.capturer = SampleCapturer(self)
        except Exception, ex:
            self.logMessage(ex.message)
        else:
            self.capturer.run()
        pass