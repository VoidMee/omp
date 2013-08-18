import wx

import ui.frames as frames

class App(wx.App):

    def OnInit(self):
        self.frame = frames.RootFrame()
        return True

    def OnExit(self):
        pass


if __name__ == "__main__":
    app = App()
    app.MainLoop()