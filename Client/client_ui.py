import wx
import login

username = ''

class RegisterTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)


class Tabs(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)
        
        registerTab = RegisterTab(self)
        self.AddPage(registerTab, "Inregistrare")
        
        othersTab = wx.Panel(self)
        self.AddPage(othersTab, "Altele")
        
class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs) 
        panel = wx.Panel(self)
        notebook = Tabs(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()

app = wx.App()

#Login section
loginDlg = login.Login(None, -1, 'Autentificare')
ret = loginDlg.ShowModal()
if ret == wx.ID_OK:
    print loginDlg.GetUserName() + ' ' + loginDlg.GetPassword()
    username = loginDlg.GetUserName()
else:
    loginDlg.Destroy()
    sys.exit()
	
loginDlg.Destroy()
		
#main frame
frame = MainFrame(None, -1, 'Client')
frame.Show()
app.MainLoop()