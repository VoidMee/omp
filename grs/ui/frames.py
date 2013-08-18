import wx

from cfg.constants import ROOTFRAMENAME
from lib.grabber import Grabber

class RootFrame(wx.Frame):

    def __init__(self):
        self._initializeComponents()
        self.Show()

    def _initializeComponents(self):
        #intialize frame
        wx.Frame.__init__(self, None, -1, ROOTFRAMENAME, pos=(10,10), size=(1000, 650), style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)

        #panel to hold controls for testing the project
        self.testPanel = wx.Panel(self, pos=(300, 0), size=(700, 500), style = wx.TAB_TRAVERSAL | wx.BORDER_SIMPLE)

        #runButton to run the Project in Development Mode
        self.runButton = wx.Button(self.testPanel, label="Start Project", pos=(500, 15), size=(150,30))
        #self.runButton = wx.Button(self, label="Start Project", pos=(700, 15), size=(160,30))
        self.Bind(wx.EVT_BUTTON, self._onStartProject, self.runButton)
        #self.runButton.SetDefault();

        #settingButton for setting the project
        self.settingButton = wx.Button(self.testPanel, label="Settings", pos=(50,15), size=(60,30))

        #panel to hold controls fot training the classifier
        self.trainPanel = wx.Panel(self, name="Train Classifier", pos=(0,0), size=(300,500), style = wx.TAB_TRAVERSAL | wx.BORDER_SIMPLE)

        #trainButton for starting the training
        self.trainButton = wx.Button(self.trainPanel, label="Star Training", pos=(50, 15), size=(160, 30))
        #self.trainButton = wx.Button(self, label="Star Training", pos=(50, 15), size=(160, 30))

        #panel to show system event outputs
        self.sysEventPanel = wx.Panel(self, name="System Log", pos=(0, 500), size=(1000, 650), style=wx.TAB_TRAVERSAL|wx.BORDER_SIMPLE)

        #sysEventLabel for displaying output events
        self.sysEventLabel = wx.StaticText(parent=self.sysEventPanel, id=-1, label="Output:", pos=(10,10))

    def _onStartProject(self, event):
        try:
            self.grabber = Grabber()
        except Exception, ex:
            self.sysEventLabel.SetLabel(ex.message)
        self.runButton.SetLabel("Stop Project")
        pass