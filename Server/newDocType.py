import wx 

import sys
sys.path.append("..\\Shared\\")
from uiPanel import UIPanel
from uiPanel import uiType

class NewDocType(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(NewDocType, self).__init__(*args, **kwargs) 
        
        panel = UIPanel(wx.Panel(self, wx.ID_ANY), '') 

        self._docType =     panel.AddLine('Tip', uiType.text)
        self._description =    panel.AddLine('Descriere', uiType.text)
        btnOK, btnCancel =  panel.AddButtons('OK', 'Cancel')

        btnOK.SetDefault()
        panel.topSizer.Fit(self)  

    def GetDocumentType(self):
        return self._docType.GetValue()

    def GetDocumentDescription(self):
        return self._description.GetValue()
