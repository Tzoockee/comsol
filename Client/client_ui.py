#WX widgets
import wx

#dialogs
import login
import changePass

#database
import database

#system
import time
import os
import shutil
import sys
from datetime import datetime

#printing
from printer import Printer

#shared
sys.path.append("..\\Shared\\")
from settings import settings
from uiPanel import UIPanel
from uiPanel import uiType
from utils import FillListCtrl
from utils import GetDateString

__version__ = 1.5
authUser = ''

def ChangePassword(authenticatedUser):
    changePwdDlg = changePass.ChangePass(database.GetUserFullName(authenticatedUser), None, -1, 'Schimbare Parola')
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
    
class RegisterTab(UIPanel):
    def __init__(self, parent):
        UIPanel.__init__(self, parent, database.GetUserFullName(authUser))

        self._docType =     self.AddLine('Tip Document', uiType.combo)
        self._date =        self.AddLine('Data', uiType.date)
        self._lastName =    self.AddLine('Nume', uiType.text)
        self._firstName =   self.AddLine('Prenume', uiType.text)
        self._path =        self.AddLine('Cale Document', uiType.filePath)
        self._description = self.AddLine('Descriere', uiType.multilineText, size = (-1, 100))
        registerBtn, =      self.AddButtons('Inregistrare')

        self.Bind(wx.EVT_BUTTON, self.OnRegister, registerBtn)
        registerBtn.SetDefault()
        self.FillDocTypes()

    def FillDocTypes(self):
        docTypes = database.GetDocumentTypes()
        for docType in docTypes:
            self._docType.Append(docType[0])
        self._docType.SetSelection(0)

    def OnRegister(self, event):
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
        destFile = os.path.join(os.path.sep, settings['docRepositoryPath'], newFileName)
        try:
            shutil.copy2(self._path.GetValue(), destFile)
        except (IOError, os.error) as why:
            wx.MessageBox(str(why), 'Error', wx.OK | wx.ICON_ERROR)
            return

        newNumber = database.AddDocument(authUser, selectedDocType, GetDateString(self._date), selectedLastName, selectedFirstName, destFile, selectedDescription)
        if newNumber == '':
            return
        
        wx.MessageBox(str(newNumber), 'Info', wx.OK | wx.ICON_INFORMATION)

        self._lastName.SetValue('')
        self._firstName.SetValue('')
        self._path.SetValue('')
        self._description.SetValue('')


class ReportTab(UIPanel):
    def __init__(self, parent):
        UIPanel.__init__(self, parent, database.GetUserFullName(authUser))

        #layout
        self._docType =                     self.AddLine('Tip Document', uiType.combo)
        self._dateFrom =                    self.AddLine('De la:', uiType.date)
        self._dateTo =                      self.AddLine('Pana la:', uiType.date)
        reportBtn, printBtn, previewBtn =   self.AddButtons('Generare', 'Tiparire', 'Pre-vizualizare')
        self._reportList =                  self.AddLine('', uiType.list)

        #events
        self.Bind(wx.EVT_BUTTON, self.OnFillReport, reportBtn)
        self.Bind(wx.EVT_BUTTON, self.OnPrintReport, printBtn)
        self.Bind(wx.EVT_BUTTON, self.OnPreviewReport, previewBtn)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnReportDblClick, self._reportList)

        #initialization
        self.FillDocTypes()

        #printer
        self._html_printer = Printer(self)
        self._html_printer.GetPrintData().SetPaperId(wx.PAPER_A4)
        self._html_printer.GetPrintData().SetOrientation(wx.LANDSCAPE)

    def FillDocTypes(self):
        docTypes = database.GetDocumentTypes()
        self._docType.Append('Toate Tipurile')
        for docType in docTypes:
            self._docType.Append(docType[0])
        self._docType.SetSelection(0)

    def GetReportContent(self):
        docTypeIndex = self._docType.GetCurrentSelection()        
        if docTypeIndex == 0:
            rows = database.GetReport(authUser, GetDateString(self._dateFrom), GetDateString(self._dateTo))
        else:
            selectedDocType = self._docType.GetString(docTypeIndex)
            rows = database.GetReportByDocType(authUser, selectedDocType, GetDateString(self._dateFrom), GetDateString(self._dateTo))
        return rows

    def OnFillReport(self, event):
        FillListCtrl(self._reportList, self.GetReportContent())

    def OnPreviewReport(self, event):
        self._html_printer.PreviewText(self.GetReportContent(), datetime.today().strftime('%A, %d. %B %Y %I:%M%p'))

    def OnPrintReport(self, event):
        self._html_printer.Print(self.GetReportContent(), datetime.today().strftime('%A, %d. %B %Y %I:%M%p'))
        
    def OnReportDblClick(self, event):
        os.system(database.GetDocument(event.GetText()))

class OthersTab(UIPanel):
    def __init__(self, parent):
        UIPanel.__init__(self, parent, database.GetUserFullName(authUser))

        changePwdBtn, = self.AddButtons('Schimbare Parola')
        self.Bind(wx.EVT_BUTTON, self.OnChangePassword, changePwdBtn)

    def OnChangePassword(self, event):
        ChangePassword(authUser)

class AboutTab(UIPanel):
    def __init__(self, parent):
        UIPanel.__init__(self, parent, database.GetUserFullName(authUser))

        self.AddImage('comsol_logo.gif')
        self.AddLine('Versiune: ' + str(__version__), uiType.staticText)

class Tabs(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)
        
        registerTab = RegisterTab(self)
        self.AddPage(registerTab, "Inregistrare")
        
        reportTab = ReportTab(self)
        self.AddPage(reportTab, "Raport")

        othersTab = OthersTab(self)
        self.AddPage(othersTab, "Altele")

        aboutTab = AboutTab(self)
        self.AddPage(aboutTab, "Despre")
        
class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs) 
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap('comsol_logo.gif', wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

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
frame = MainFrame(None, -1, 'Registratura Electronica by Comsol')
frame.Show()
app.MainLoop()
