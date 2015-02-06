import wx 
import newUser
import newDocType
import pyodbc
import database

import sys
sys.path.append("..\\Shared\\")
from uiPanel import UIPanel
from uiPanel import uiType

def FillListCtrl(listCtrl, rows):
    listCtrl.ClearAll()

    if len(rows) == 0:
        return
        
    for index, column in enumerate(rows[0].cursor_description):
        listCtrl.InsertColumn(index+1, column[0])
            
    for indexRow, row in enumerate(rows):
        listCtrl.InsertStringItem(indexRow, str(row[0]))
        for indexCol in range(1, len(row.cursor_description)):
            listCtrl.SetStringItem(indexRow, indexCol, str(row[indexCol]))

class UsersTab(UIPanel):
    def __init__(self, parent):
        UIPanel.__init__(self, parent, '')
        
        self._userList = self.AddLine('', uiType.list)
        newBtn, deleteBtn = self.AddButtons('Adauga', 'Sterge')

        #events
        self.Bind(wx.EVT_BUTTON, self.OnNewUser, newBtn)
        self.Bind(wx.EVT_BUTTON, self.OnDeleteUser, deleteBtn)
        
        #initialize
        self.RefreshUserList()

    def OnNewUser(self, event):
        newUserDlg = newUser.NewUser(None, -1, 'Utilizator nou')
        ret = newUserDlg.ShowModal()        
        if ret == wx.ID_OK:
            database.AddNewUser(newUserDlg.GetUserName(), newUserDlg.GetFirstName(), newUserDlg.GetLastName())
            self.RefreshUserList()
        newUserDlg.Destroy()
        
    def OnDeleteUser(self, event):
        index = self._userList.GetFirstSelected()
        if index != -1 :
            database.DeleteUser(self._userList.GetItem(index, 0).GetText())
            self.RefreshUserList()
        
    def RefreshUserList(self):
        rows = database.GetUsers()
        FillListCtrl(self._userList, rows)

class DocTypeTab(UIPanel):
    def __init__(self, parent):
        UIPanel.__init__(self, parent)

        self._docTypeList = self.AddLine('', uiType.list)
        newBtn, deleteBtn = self.AddButtons('Adauga', 'Sterge')

        #events
        self.Bind(wx.EVT_BUTTON, self.OnNewDocType, newBtn)
        self.Bind(wx.EVT_BUTTON, self.OnDeleteDocType, deleteBtn)
        
        #initialize
        self.RefreshDocTypeList()

    def RefreshDocTypeList(self):
        FillListCtrl(self._docTypeList, database.GetDocTypes())

    def OnNewDocType(self, event):
        newDocTypeDlg = newDocType.NewDocType(None, -1, 'Tip Document Nou')
        ret = newDocTypeDlg.ShowModal()        
        if ret == wx.ID_OK:
            database.AddNewDocType(newDocTypeDlg.GetDocumentType(), newDocTypeDlg.GetDocumentDescription())
            self.RefreshDocTypeList()
        newDocTypeDlg.Destroy()

    def OnDeleteDocType(self, event):
        index = self._docTypeList.GetFirstSelected()
        if index != -1 :
            database.DeleteDocType(self._docTypeList.GetItem(index, 0).GetText())
            self.RefreshDocTypeList()		

class Tabs(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)
        
        usersTab = UsersTab(self)
        self.AddPage(usersTab, "Utilizatori")
        
        docsTab = DocTypeTab(self)
        self.AddPage(docsTab, "Documente")
        
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
frame = MainFrame(None, -1, 'Admin')
frame.Show()
app.MainLoop()