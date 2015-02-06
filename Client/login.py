import wx 
import sys
sys.path.append("..\\Shared\\")
from uiPanel import UIPanel
from uiPanel import uiType

class Login(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs) 

        panel = UIPanel(wx.Panel(self, wx.ID_ANY), user = '') 
        self._user =        panel.AddLine('Utilizator', uiType.text)
        self._password =    panel.AddLine('Parola', uiType.password)
        okBtn, cancelBtn =  panel.AddButtons('OK', 'Cancel')

        okBtn.SetDefault()
        panel.topSizer.Fit(self)

    def GetUserName(self):
        return self._user.GetValue()

    def GetPassword(self):
        return self._password.GetValue()
