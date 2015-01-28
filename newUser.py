import wx 

class NewUser(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(NewUser, self).__init__(*args, **kwargs) 
        
        # Add a panel so it looks correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)
 
        labelName = wx.StaticText(self.panel, wx.ID_ANY, 'Nume')
        self._lastName = wx.TextCtrl(self.panel, wx.ID_ANY, '')
 
        labelFirstName = wx.StaticText(self.panel, wx.ID_ANY, 'Prenume')
        self._firstName = wx.TextCtrl(self.panel, wx.ID_ANY, '')
 
        labelUserName = wx.StaticText(self.panel, wx.ID_ANY, 'Utilizator')
        self._userName = wx.TextCtrl(self.panel, wx.ID_ANY, '')
 
        okBtn = wx.Button(self.panel, wx.ID_OK, 'OK')        
        cancelBtn = wx.Button(self.panel, wx.ID_CANCEL, 'Cancel')
 
        topSizer        = wx.BoxSizer(wx.VERTICAL)
        inputOneSizer   = wx.BoxSizer(wx.HORIZONTAL)
        inputTwoSizer   = wx.BoxSizer(wx.HORIZONTAL)
        inputThreeSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer        = wx.BoxSizer(wx.HORIZONTAL)
 
        inputOneSizer.Add(labelName, 0, wx.ALL, 5)
        inputOneSizer.Add(self._lastName, 1, wx.ALL|wx.EXPAND, 5)
 
        inputTwoSizer.Add(labelFirstName, 0, wx.ALL, 5)
        inputTwoSizer.Add(self._firstName, 1, wx.ALL|wx.EXPAND, 5)
 
        inputThreeSizer.Add(labelUserName, 0, wx.ALL, 5)
        inputThreeSizer.Add(self._userName, 1, wx.ALL|wx.EXPAND, 5)
 
        btnSizer.Add(okBtn, 0, wx.ALL, 5)
        btnSizer.Add(cancelBtn, 0, wx.ALL, 5)
 
        topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(inputOneSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(inputTwoSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(inputThreeSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btnSizer, 0, wx.ALL|wx.CENTER, 5)
 
        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)
        

    def GetUserName(self):
        return self._userName.GetValue()

    def GetFirstName(self):
        return self._firstName.GetValue()

    def GetLastName(self):
        return self._lastName.GetValue()