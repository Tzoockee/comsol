import wx 
import uiPanel

class ChangePass(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(ChangePass, self).__init__(*args, **kwargs) 
        
        panel = uiPanel.UIPanel(wx.Panel(self, wx.ID_ANY), user = '') 

        self._oldPass =     panel.AddLine('Parola veche', uiPanel.uiType.password)
        self._newPass1 =    panel.AddLine('Parola noua', uiPanel.uiType.password)
        self._newPass2 =    panel.AddLine('Parola noua', uiPanel.uiType.password)
        btnOK, btnCancel =  panel.AddButtons('OK', 'Cancel')

        self.Bind(wx.EVT_BUTTON, self.OnOK, btnOK)
        btnOK.SetDefault()

        panel.topSizer.Fit(self)

    def OnOK(self, event):
        if self._newPass1.GetValue() != self._newPass2.GetValue() or self._newPass1.GetValue() == '':
            wx.MessageBox('Parolele nu se potrivesc', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            event.Skip()

    def GetOldPassword(self):
        return self._oldPass.GetValue()

    def GetNewPassword(self):
        return self._newPass1.GetValue()
