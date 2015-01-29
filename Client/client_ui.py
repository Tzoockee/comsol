import wx
import login
from datetime import datetime
import time
import os
import shutil

username = ''
docRepositoryPath = 'C:\\Temp\\'

class RegisterTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        labelDocType = wx.StaticText(self, wx.ID_ANY, 'Tip Document')
        self._docType = wx.ComboBox(self, -1, style = wx.CB_READONLY)
 
        labelDate = wx.StaticText(self, wx.ID_ANY, 'Data')
        self._date = wx.DatePickerCtrl(self, wx.ID_ANY, style = wx.DP_DEFAULT | wx.DP_DROPDOWN)

        labelPath = wx.StaticText(self, wx.ID_ANY, 'Cale Document')
        self._path = wx.TextCtrl(self, wx.ID_ANY, '', style = wx.TE_READONLY)
        browseBtn = wx.Button(self, wx.ID_ANY, 'Browse')  

        registerBtn = wx.Button(self, wx.ID_OK, 'Inregistrare')        
 
        topSizer        = wx.BoxSizer(wx.VERTICAL)
        inputOneSizer   = wx.BoxSizer(wx.HORIZONTAL)
        inputTwoSizer   = wx.BoxSizer(wx.HORIZONTAL)
        inputThreeSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer        = wx.BoxSizer(wx.HORIZONTAL)
 
        inputOneSizer.Add(labelDocType, 0, wx.ALL, 5)
        inputOneSizer.Add(self._docType, 1, wx.ALL|wx.EXPAND, 5)
 
        inputTwoSizer.Add(labelDate, 0, wx.ALL, 5)
        inputTwoSizer.Add(self._date, 1, wx.ALL|wx.EXPAND, 5)
		
        inputThreeSizer.Add(labelPath, 0, wx.ALL, 5)
        inputThreeSizer.Add(self._path, 1, wx.ALL|wx.EXPAND, 5)
        inputThreeSizer.Add(browseBtn, 1, wx.ALL|wx.EXPAND, 5)
 
        btnSizer.Add(registerBtn, 0, wx.CENTER, 5)
 
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticText(self, wx.ID_ANY, username), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(inputOneSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(inputTwoSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(inputThreeSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btnSizer, 0, wx.ALL|wx.CENTER, 5)
 
        self.SetSizer(topSizer)
        topSizer.Fit(self)

        #events
        self.Bind(wx.EVT_BUTTON, self.OnFileBrowse, browseBtn)
        self.Bind(wx.EVT_BUTTON, self.OnRegister, registerBtn)
		
        #initialize
        self.FillDocTypes()
    
    def FillDocTypes(self):
        self._docType.Append('Tip 1')
        self._docType.Append('Tip 2')
        self._docType.SetSelection(0)
		
    def OnFileBrowse(self, event):
        dialog = wx.FileDialog(self, "Selectati fisierul...", "", "", "Word files (*.doc)|*.doc|PDF files (*.pdf)|*.pdf", wx.FD_OPEN | wx.FD_CHANGE_DIR)
        if dialog.ShowModal() == wx.ID_OK:
            self._path.SetValue(str(dialog.GetPath()))
        dialog.Destroy()

    def OnRegister(self, event):
        #First copy the file and get the new name and path
        #https://msdn.microsoft.com/en-us/library/aa259188(SQL.80).aspx
        selectedDocType = self._docType.GetString(self._docType.GetCurrentSelection())
        selectedYear = str(self._date.GetValue().Year)
        selectedMonth = str(self._date.GetValue().Month+1)
        selectedDay = str(self._date.GetValue().Day)
        selectedFile = str(self._path.GetValue())

        print 'Selected User: 							' + username
        print 'Selected Document type: 					' + selectedDocType
        print 'Selected Date: 							' + selectedDay + '/' + selectedMonth + '/' + selectedYear
        print 'Selected File: 							' + selectedFile

        dirName = os.path.dirname(selectedFile)
        fileNameWithExt = os.path.basename(selectedFile)
        fileName, fileExtension = os.path.splitext(fileNameWithExt)
        newFileName = username + '_' + selectedYear + '_' + selectedMonth + '_' + selectedDay + '_' + str(time.time()).replace('.', '_') + fileExtension
        destFile = os.path.join(os.path.sep, docRepositoryPath, newFileName)
        print 'Destination File: 						' + destFile
        try:
            shutil.copy2(self._path.GetValue(), destFile)
        except (IOError, os.error) as why:
            wx.MessageBox(str(why), 'Error', wx.OK | wx.ICON_ERROR)
		
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
    username = loginDlg.GetUserName()
else:
    loginDlg.Destroy()
    sys.exit()
	
loginDlg.Destroy()
		
#main frame
frame = MainFrame(None, -1, 'Client')
frame.Show()
app.MainLoop()