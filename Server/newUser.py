import wx 
import sys
sys.path.append("..\\Shared\\")
from uiPanel import UIPanel
from uiPanel import uiType

class NewUser(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(NewUser, self).__init__(*args, **kwargs) 

        panel = UIPanel(wx.Panel(self, wx.ID_ANY), '') 

        self._lastName =     panel.AddLine('Nume', uiType.text)
        self._firstName =    panel.AddLine('Prenume', uiType.text)
        self._userName =    panel.AddLine('Utilizator', uiType.text)
        btnOK, btnCancel =  panel.AddButtons('OK', 'Cancel')

        btnOK.SetDefault()
        panel.topSizer.Fit(self)  
        
    def GetUserName(self):
        return self._userName.GetValue()

    def GetFirstName(self):
        return self._firstName.GetValue()

    def GetLastName(self):
        return self._lastName.GetValue()      
