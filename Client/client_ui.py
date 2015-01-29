import wx

import login
import changePass
import client_cfg
import database

from datetime import datetime
import time
import os
import shutil
import sys

authUser = ''


class RegisterTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        labelDocType = wx.StaticText(self, wx.ID_ANY, 'Tip Document')
        self._docType = wx.ComboBox(self, -1, style = wx.CB_READONLY)
 
        labelDate = wx.StaticText(self, wx.ID_ANY, 'Data')
        self._date = wx.DatePickerCtrl(self, wx.ID_ANY, style = wx.DP_DEFAULT | wx.DP_DROPDOWN)

        labelPath = wx.StaticText(self, wx.ID_ANY, 'Cale Document')
        self._path = wx.TextCtrl(self, wx.ID_ANY, '', style = wx.TE_READONLY)
        browseBtn = wx.Button(self, wx.ID_ANY, '...')  

        labelDesc = wx.StaticText(self, wx.ID_ANY, 'Descriere')
        self._description = wx.TextCtrl(self, wx.ID_ANY, '', style = wx.TE_MULTILINE, size = (-1, 100))

        labelLastName = wx.StaticText(self, wx.ID_ANY, 'Nume')
        self._lastName = wx.TextCtrl(self, wx.ID_ANY, '')
		
        labelFirstName = wx.StaticText(self, wx.ID_ANY, 'Prenume')
        self._firstName = wx.TextCtrl(self, wx.ID_ANY, '')
		
        registerBtn = wx.Button(self, wx.ID_OK, 'Inregistrare')        
 
        topSizer        = wx.BoxSizer(wx.VERTICAL)
        sizerDocType    = wx.BoxSizer(wx.HORIZONTAL)
        sizerDate       = wx.BoxSizer(wx.HORIZONTAL)
        sizerPath       = wx.BoxSizer(wx.HORIZONTAL)
        sizerDesc       = wx.BoxSizer(wx.HORIZONTAL)
        sizerLastName   = wx.BoxSizer(wx.HORIZONTAL)
        sizerFirstName  = wx.BoxSizer(wx.HORIZONTAL)		
        btnSizer        = wx.BoxSizer(wx.HORIZONTAL)
 
        sizerDocType.Add(labelDocType, 0, wx.ALL, 5)
        sizerDocType.Add(self._docType, 1, wx.ALL|wx.EXPAND, 5)
 
        sizerDate.Add(labelDate, 0, wx.ALL, 5)
        sizerDate.Add(self._date, 1, wx.ALL|wx.EXPAND, 5)
		
        sizerPath.Add(labelPath, 0, wx.ALL, 5)
        sizerPath.Add(self._path, 1, wx.ALL|wx.EXPAND, 5)
        sizerPath.Add(browseBtn, 1, wx.ALL, 5)
 
        sizerDesc.Add(labelDesc, 0, wx.ALL, 5)
        sizerDesc.Add(self._description, 1, wx.ALL|wx.EXPAND, 5)
 
        sizerLastName.Add(labelLastName, 0, wx.ALL, 5)
        sizerLastName.Add(self._lastName, 1, wx.ALL|wx.EXPAND, 5)

        sizerFirstName.Add(labelFirstName, 0, wx.ALL, 5)
        sizerFirstName.Add(self._firstName, 1, wx.ALL|wx.EXPAND, 5)
		
        btnSizer.Add(registerBtn, 0, wx.CENTER, 5)
 
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticText(self, wx.ID_ANY, database.GetUserFullName(authUser)), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(sizerDocType, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(sizerDate, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(sizerLastName, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(sizerFirstName, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(sizerPath, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(sizerDesc, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btnSizer, 0, wx.ALL|wx.CENTER, 5)
 
        self.SetSizer(topSizer)
        topSizer.Fit(self)
        registerBtn.SetDefault()

        #events
        self.Bind(wx.EVT_BUTTON, self.OnFileBrowse, browseBtn)
        self.Bind(wx.EVT_BUTTON, self.OnRegister, registerBtn)
		
        #initialize
        self.FillDocTypes()
    
    def FillDocTypes(self):
        docTypes = database.GetDocumentTypes()
        for docType in docTypes:
            self._docType.Append(docType[0])
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
        selectedDescription = self._description.GetValue()
        selectedLastName = self._lastName.GetValue()
        selectedFirstName = self._firstName.GetValue()

        print 'Selected User: 							' + authUser
        print 'Selected Document type: 					' + selectedDocType
        print 'Selected Date: 							' + selectedDay + '/' + selectedMonth + '/' + selectedYear
        print 'Selected Last Name: 						' + selectedLastName
        print 'Selected First Name: 					' + selectedFirstName
        print 'Selected File: 							' + selectedFile
        print 'Selected Description: 					' + selectedDescription

        dirName = os.path.dirname(selectedFile)
        fileNameWithExt = os.path.basename(selectedFile)
        fileName, fileExtension = os.path.splitext(fileNameWithExt)
        newFileName = authUser + '_' + selectedYear + '_' + selectedMonth + '_' + selectedDay + '_' + str(time.time()).replace('.', '_') + fileExtension
        destFile = os.path.join(os.path.sep, client_cfg.docRepositoryPath, newFileName)
        print 'Destination File: 						' + destFile
        try:
            shutil.copy2(self._path.GetValue(), destFile)
        except (IOError, os.error) as why:
            wx.MessageBox(str(why), 'Error', wx.OK | wx.ICON_ERROR)

class OthersTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        changePwdBtn = wx.Button(self, wx.ID_ANY, 'Schimbare Parola')
		
        topSizer        = wx.BoxSizer(wx.VERTICAL)
        sizerBtn        = wx.BoxSizer(wx.HORIZONTAL)			
		
        sizerBtn.Add(changePwdBtn, 0, wx.ALL, 5)

        topSizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticText(self, wx.ID_ANY, database.GetUserFullName(authUser)), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(sizerBtn, 0, wx.ALL|wx.EXPAND, 5)
 
        self.SetSizer(topSizer)
        topSizer.Fit(self)

        #events
        self.Bind(wx.EVT_BUTTON, self.OnChangePassword, changePwdBtn)

    def OnChangePassword(self, event):
        changePwdDlg = changePass.ChangePass(None, -1, 'Schimbare Parola')
        ret = changePwdDlg.ShowModal()        
        if ret == wx.ID_OK:
            print changePwdDlg.GetOldPassword()
            print changePwdDlg.GetNewPassword()
        changePwdDlg.Destroy()

class Tabs(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)
        
        registerTab = RegisterTab(self)
        self.AddPage(registerTab, "Inregistrare")
        
        othersTab = OthersTab(self)
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
    if database.TestLogin(loginDlg.GetUserName(), loginDlg.GetPassword()):
        authUser = loginDlg.GetUserName()
    else:
        wx.MessageBox('Autentificare esuata', 'Error', wx.OK | wx.ICON_ERROR)
        loginDlg.Destroy()
        sys.exit()
else:
    loginDlg.Destroy()
    sys.exit()

loginDlg.Destroy()
		
#main frame
frame = MainFrame(None, -1, 'Client')
frame.Show()
app.MainLoop()