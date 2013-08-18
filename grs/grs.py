import wx

from ui.frames import RootFrame
#from sys.grabber import Grabber

class App(wx.App):

    def OnInit(self):
        self.frame = RootFrame()
        return True

    def OnExit(self):
        pass


if __name__ == "__main__":
    app = App()
    app.MainLoop()