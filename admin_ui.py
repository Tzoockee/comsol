import wx 
import newUser
import pyodbc
import database

class UsersTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        #users list control
        self._userList = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self._userList.InsertColumn(1, 'Utilizator')
        self._userList.InsertColumn(2, 'Nume')
        self._userList.InsertColumn(3, 'Prenume')
  
        #buttons
        newBtn = wx.Button(self, wx.ID_ANY, 'Adauga')
        deleteBtn = wx.Button(self, wx.ID_ANY, 'Sterge')                
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(newBtn, 0, wx.ALL, 5)
        btnSizer.Add(deleteBtn, 0, wx.ALL, 5)
  
        #layout
        topSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer.Add(wx.StaticText(self, wx.ID_ANY, 'Utilizatori'), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(self._userList, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btnSizer, 0, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(topSizer)
        topSizer.Fit(self)
        
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
        index = 0
        
    def RefreshUserList(self):
        self._userList.DeleteAllItems()
        conn = pyodbc.connect(database.connString, autocommit=True)
        curs = conn.cursor()
        curs.execute('SELECT username, firstname, lastname FROM USERS')
        index = 0
        for row in curs:
            self._userList.InsertStringItem(index, str(row.username))
            self._userList.SetStringItem(index, 1, str(row.firstname))
            self._userList.SetStringItem(index, 2, str(row.lastname))
            index = index + 1
        conn.close()
        
class Tabs(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)
        
        usersTab = UsersTab(self)
        self.AddPage(usersTab, "Utilizatori")
        
        docsTab = wx.Panel(self)
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