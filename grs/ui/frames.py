import wx

from cfg.constants import ROOTFRAMENAME

class RootFrame(wx.Frame):

    def __init__(self):
        self._initializeComponents()
        self.Show()

    def StartGrabbing(self, event):
        print "Start Grabbing is called\n"
        self._fgr.start()
        self._fpr.start()

    def _initializeComponents(self):
        wx.Frame.__init__(self, None, -1, ROOTFRAMENAME, size=(300, 100))
        panel = wx.Panel(self)
        startButton = wx.Button(panel, label="Start", pos=(50, 15), size=(60,30))
        settingButton = wx.Button(panel, label="Settings", pos=(200,15), size=(60,30))