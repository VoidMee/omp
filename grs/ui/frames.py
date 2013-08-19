import wx
import cv2

import numpy as np

from cfg.constants import ROOTFRAMENAME
from lib.grabber import Grabber

class RootFrame(wx.Frame):

    def __init__(self, parent):
        self.parent = parent
        self._initializeComponents()
        self.Show()

    def _initializeComponents(self):
        #intialize frame
        wx.Frame.__init__(self, None, -1, ROOTFRAMENAME, pos=(10,10), size=(1000, 650), style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)

        #panel to hold controls for testing the project
        self.trainPanel = wx.Panel(self, pos=(300, 0), size=(700, 500), style = wx.TAB_TRAVERSAL | wx.BORDER_SIMPLE)

        #runButton to run the Project in Development Mode
        self.runButton = wx.Button(self.trainPanel, label="Start Training", pos=(500, 15), size=(150,30))
        #self.runButton = wx.Button(self, label="Start Project", pos=(700, 15), size=(160,30))
        self.Bind(wx.EVT_BUTTON, self._onOpen, self.runButton)
        #self.runButton.SetDefault();

        self.fileUploadLabel = wx.StaticText(parent=self.trainPanel, id=-1, label="Upload Image Data to train:", pos=(50, 70))
        self.fileUploadButton = wx.Button(parent=self.trainPanel, label="Browse", pos=(220, 60), size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self._onOpen, self.fileUploadButton)
        #self.fileUploadDialog = wx.FileDialog(parent=self.testPanel, message="Choose a file", defaultDir="", defaultFile="", wildcard="*.*", style=0)

        #settingButton for setting the project
        self.settingButton = wx.Button(self.trainPanel, label="Settings", pos=(50,15), size=(60,30))

        #panel to hold controls fot training the classifier
        self.testPanel = wx.Panel(self, name="Train Classifier", pos=(0,0), size=(300,500), style = wx.TAB_TRAVERSAL | wx.BORDER_SIMPLE)

        #trainButton for starting the training
        self.trainButton = wx.Button(self.testPanel, label="Star Project", pos=(50, 15), size=(160, 30))
        #self.trainButton = wx.Button(self, label="Star Training", pos=(50, 15), size=(160, 30))

        #panel to show system event outputs
        self.sysEventPanel = wx.Panel(self, name="System Log", pos=(0, 500), size=(1000, 650), style=wx.TAB_TRAVERSAL|wx.BORDER_SIMPLE)

        #sysEventLabel for displaying output events
        self.sysEventLabel = wx.StaticText(parent=self.sysEventPanel, id=-1, label="Output:", pos=(10,10))




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
        saveFileDialog = wx.FileDialog(self, "Save XYZ file", "", "", "JPEG (*.jpg)|*.jpg|Bitmap (*.bmp)|*.bmp|PNG (*.png)|*.png", wx.FD_OPEN | wx.CHANGE_DIR | wx.MULTIPLE)
        retVal = saveFileDialog.ShowModal()
        if retVal == wx.ID_CANCEL:
            self.sysEventLabel.SetLabel("You Pressed Cancel")
            #return     # the user changed idea...
        elif retVal == wx.ID_OK:
            outString = saveFileDialog.GetDirectory() + ": "
            for item in saveFileDialog.GetFilenames():
                outString += item
            self.sysEventLabel.SetLabel(outString)
        return
