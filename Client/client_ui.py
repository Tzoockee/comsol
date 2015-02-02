import wx

import login
import changePass
import client_cfg
import database

from prettytable import PrettyTable

from datetime import datetime
import time
import os
import shutil
import sys

authUser = ''

def FillListCtrl(listCtrl, rows):
    listCtrl.ClearAll()

    if len(rows) == 0:
        return
        
    for index, column in enumerate(rows[0].cursor_description):
        listCtrl.InsertColumn(index+1, column[0])
            
    for indexRow, row in enumerate(rows):
        listCtrl.InsertStringItem(indexRow, str(row[0]))
        for indexCol, column in enumerate(row.cursor_description[1:]):
            listCtrl.SetStringItem(indexRow, indexCol, str(row[indexCol]))

def PrintReport(rows):
    if len(rows) == 0:
        return
    
    col_names = [cn[0] for cn in rows[0].cursor_description]
    x = PrettyTable(col_names)
    for row in rows:
        x.add_row(row)

    t = open('Report.txt', 'w')
    t.write(x.get_string())
    t.close()
    os.system('notepad.exe /P Report.txt')
    os.system('rm Report.txt')


def ChangePassword(authenticatedUser):
    changePwdDlg = changePass.ChangePass(None, -1, 'Schimbare Parola')
    ret = changePwdDlg.ShowModal()        
    if ret == wx.ID_OK:
        if database.TestLogin(authenticatedUser, changePwdDlg.GetOldPassword()):
            database.ChangePassword(authenticatedUser, changePwdDlg.GetNewPassword())
            wx.MessageBox('Parola a fost schimbata', 'Parola', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox('Autentificare esuata', 'Error', wx.OK | wx.ICON_ERROR)
    changePwdDlg.Destroy()

def DoLogin():
    loginDlg = login.Login(None, -1, 'Autentificare')
    ret = loginDlg.ShowModal()
    authenticatedUser = ''
    if ret == wx.ID_OK:
        if database.TestLogin(loginDlg.GetUserName(), loginDlg.GetPassword()):
            authenticatedUser = loginDlg.GetUserName()
        else:
            wx.MessageBox('Autentificare esuata', 'Error', wx.OK | wx.ICON_ERROR)
            loginDlg.Destroy()
            sys.exit()
    else:
        loginDlg.Destroy()
        sys.exit()
    password = loginDlg.GetPassword()
    loginDlg.Destroy()
    if password == authenticatedUser:
        ChangePassword(authenticatedUser)
    return authenticatedUser
    
def GetDateString(dateCtrl):
    selectedYear = str(dateCtrl.GetValue().Year)
    selectedMonth = str(dateCtrl.GetValue().Month+1)
    selectedDay = str(dateCtrl.GetValue().Day)
    return selectedDay + '/' + selectedMonth + '/' + selectedYear

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
        dialog = wx.FileDialog(self, "Selectati fisierul...", "", "", "Word files (*.doc)|*.doc|PDF files (*.pdf)|*.pdf|All files (*.*)|*.*", wx.FD_OPEN | wx.FD_CHANGE_DIR)
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

        if selectedFile == '' or selectedDescription == '' or selectedLastName == '' or selectedFirstName == '':
            wx.MessageBox('Nu toate campurile sunt completate', 'Error', wx.OK | wx.ICON_ERROR)
            return

        dirName = os.path.dirname(selectedFile)
        fileNameWithExt = os.path.basename(selectedFile)
        fileName, fileExtension = os.path.splitext(fileNameWithExt)
        newFileName = authUser + '_' + selectedYear + '_' + selectedMonth + '_' + selectedDay + '_' + str(time.time()).replace('.', '_') + fileExtension
        destFile = os.path.join(os.path.sep, client_cfg.docRepositoryPath, newFileName)
        try:
            shutil.copy2(self._path.GetValue(), destFile)
        except (IOError, os.error) as why:
            wx.MessageBox(str(why), 'Error', wx.OK | wx.ICON_ERROR)
            return

        newNumber = database.AddDocument(authUser, selectedDocType, GetDateString(self._date), selectedLastName, selectedFirstName, destFile, selectedDescription)
        if newNumber == '':
            return
        
        wx.MessageBox(str(newNumber), 'Error', wx.OK | wx.ICON_INFORMATION)

        self._lastName.SetValue('')
        self._firstName.SetValue('')
        self._path.SetValue('')
        self._description.SetValue('')

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
        ChangePassword(authUser)


class ReportTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        labelDocType = wx.StaticText(self, wx.ID_ANY, 'Tip Document')
        self._docType = wx.ComboBox(self, -1, style = wx.CB_READONLY)

        labelDateFrom = wx.StaticText(self, wx.ID_ANY, 'De la:')
        self._dateFrom = wx.DatePickerCtrl(self, wx.ID_ANY, style = wx.DP_DEFAULT | wx.DP_DROPDOWN)

        labelDateTo = wx.StaticText(self, wx.ID_ANY, 'Pana la:')
        self._dateTo = wx.DatePickerCtrl(self, wx.ID_ANY, style = wx.DP_DEFAULT | wx.DP_DROPDOWN)

        reportBtn = wx.Button(self, wx.ID_ANY, 'Genereaza')
        printBtn = wx.Button(self, wx.ID_ANY, 'Tipareste')        

        self._reportList = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)

        topSizer        = wx.BoxSizer(wx.VERTICAL)        

        sizerDocType    = wx.BoxSizer(wx.HORIZONTAL)
        sizerDocType.Add(labelDocType, 0, wx.ALL, 5)
        sizerDocType.Add(self._docType, 1, wx.ALL|wx.EXPAND, 5)

        sizerDateFrom    = wx.BoxSizer(wx.HORIZONTAL)
        sizerDateFrom.Add(labelDateFrom, 0, wx.ALL, 5)
        sizerDateFrom.Add(self._dateFrom, 1, wx.ALL|wx.EXPAND, 5)

        sizerDateTo      = wx.BoxSizer(wx.HORIZONTAL)
        sizerDateTo.Add(labelDateTo, 0, wx.ALL, 5)
        sizerDateTo.Add(self._dateTo, 1, wx.ALL|wx.EXPAND, 5)

        sizerBtn         = wx.BoxSizer(wx.HORIZONTAL)
        sizerBtn.Add(reportBtn, 0, wx.ALL, 5)
        sizerBtn.Add(printBtn, 0, wx.ALL, 5)

        topSizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticText(self, wx.ID_ANY, database.GetUserFullName(authUser)), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(sizerDocType, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(sizerDateFrom, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(sizerDateTo, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(sizerBtn, 0, wx.CENTER, 5)
        topSizer.Add(self._reportList, 0, wx.ALL|wx.EXPAND, 5)
 
        self.SetSizer(topSizer)
        topSizer.Fit(self)

        #events
        self.Bind(wx.EVT_BUTTON, self.OnFillReport, reportBtn)
        self.Bind(wx.EVT_BUTTON, self.OnPrintReport, printBtn)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnReportDblClick, self._reportList)

        #initialization
        self.FillDocTypes()

    def FillDocTypes(self):
        docTypes = database.GetDocumentTypes()
        for docType in docTypes:
            self._docType.Append(docType[0])
        self._docType.SetSelection(0)

    def OnFillReport(self, event):
        selectedDocType = self._docType.GetString(self._docType.GetCurrentSelection())
        rows = database.GetReport(authUser, selectedDocType, GetDateString(self._dateFrom), GetDateString(self._dateTo))
        FillListCtrl(self._reportList, rows)

    def OnPrintReport(self, event):
        selectedDocType = self._docType.GetString(self._docType.GetCurrentSelection())
        rows = database.GetReport(authUser, selectedDocType, GetDateString(self._dateFrom), GetDateString(self._dateTo))
        PrintReport(rows)
        
    def OnReportDblClick(self, event):
        filePath = database.GetDocument(event.GetText())
        os.system(filePath)

class Tabs(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)
        
        registerTab = RegisterTab(self)
        self.AddPage(registerTab, "Inregistrare")
        
        othersTab = OthersTab(self)
        self.AddPage(othersTab, "Altele")

        reportTab = ReportTab(self)
        self.AddPage(reportTab, "Raport")
        
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
authUser = DoLogin()
		
#main frame
frame = MainFrame(None, -1, 'Client')
frame.Show()
app.MainLoop()