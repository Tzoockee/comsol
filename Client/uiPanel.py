import wx

class uiType:
    text = 1
    password = 2
    multilineText = 3
    combo = 4
    date = 5
    filePath = 6
    list = 7

class UIPanel(wx.Panel):
    def __init__(self, parent, user=''):
        wx.Panel.__init__(self, parent)
        self.topSizer        = wx.BoxSizer(wx.VERTICAL)
        self.topSizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        self.topSizer.Add(wx.StaticText(self, wx.ID_ANY, user), 0, wx.ALL|wx.EXPAND, 5)
        self.topSizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(self.topSizer)
        self.topSizer.Fit(self)

    def AddLine(self, label, type, size = (-1, -1)):
        if type == uiType.text:
            l = wx.StaticText(self, wx.ID_ANY, label)
            editor = wx.TextCtrl(self, wx.ID_ANY, '', size = size)
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(l, 0, wx.ALL, 5)
            sizer.Add(editor, 1, wx.ALL|wx.EXPAND, 5)
            self.topSizer.Add(sizer, 0, wx.ALL|wx.EXPAND, 5)
            self.topSizer.Fit(self)
            return editor
        if type == uiType.password:
            l = wx.StaticText(self, wx.ID_ANY, label)
            editor = wx.TextCtrl(self, wx.ID_ANY, '', style = wx.TE_PASSWORD, size = size)
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(l, 0, wx.ALL, 5)
            sizer.Add(editor, 1, wx.ALL|wx.EXPAND, 5)
            self.topSizer.Add(sizer, 0, wx.ALL|wx.EXPAND, 5)
            self.topSizer.Fit(self)
            return editor
        if type == uiType.multilineText:
            l = wx.StaticText(self, wx.ID_ANY, label)
            editor = wx.TextCtrl(self, wx.ID_ANY, '', style = wx.TE_MULTILINE, size = size)
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(l, 0, wx.ALL, 5)
            sizer.Add(editor, 1, wx.ALL|wx.EXPAND, 5)
            self.topSizer.Add(sizer, 0, wx.ALL|wx.EXPAND, 5)
            self.topSizer.Fit(self)
            return editor
        if type == uiType.combo:
            l = wx.StaticText(self, wx.ID_ANY, label)
            combo = wx.ComboBox(self, -1, style = wx.CB_READONLY, size = size)
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(l, 0, wx.ALL, 5)
            sizer.Add(combo, 1, wx.ALL|wx.EXPAND, 5)
            self.topSizer.Add(sizer, 0, wx.ALL|wx.EXPAND, 5)
            self.topSizer.Fit(self)
            return combo
        if type == uiType.date:
            l = wx.StaticText(self, wx.ID_ANY, label)
            date = wx.DatePickerCtrl(self, wx.ID_ANY, style = wx.DP_DEFAULT | wx.DP_DROPDOWN, size = size)
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(l, 0, wx.ALL, 5)
            sizer.Add(date, 1, wx.ALL|wx.EXPAND, 5)
            self.topSizer.Add(sizer, 0, wx.ALL|wx.EXPAND, 5)
            self.topSizer.Fit(self)
            return date
        if type == uiType.filePath:
            l = wx.StaticText(self, wx.ID_ANY, label)
            path = wx.TextCtrl(self, wx.ID_ANY, '', style = wx.TE_READONLY, size = size)
            browseBtn = wx.Button(self, wx.ID_ANY, '...')  
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(l, 0, wx.ALL, 5)
            sizer.Add(path, 1, wx.ALL|wx.EXPAND, 5)
            sizer.Add(browseBtn, 1, wx.ALL, 5)
            self.topSizer.Add(sizer, 0, wx.ALL|wx.EXPAND, 5)
            self.topSizer.Fit(self)
            self.Bind(wx.EVT_BUTTON, lambda event: self.OnFileBrowse(event, path), browseBtn)
            return path
        if type == uiType.list:
            list = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
            self.topSizer.Add(list, 0, wx.ALL|wx.EXPAND, 5)
            self.topSizer.Fit(self)
            return list            
        return None

    def AddButtons(self, *buttons):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonList = []
        for buttonLabel in buttons:
            id = wx.ID_ANY
            if buttonLabel == 'OK':
                id = wx.ID_OK
            if buttonLabel == 'Cancel':
                id = wx.ID_CANCEL
            button = wx.Button(self, id, buttonLabel)
            sizer.Add(button, 0, wx.ALL, 5)
            buttonList.append(button)
        self.topSizer.Add(sizer, 0, wx.ALL|wx.CENTER, 5)
        self.topSizer.Fit(self)
        return buttonList

    def OnFileBrowse(self, event, path):
        dialog = wx.FileDialog(self, "Selectati fisierul...", "", "", "Word files (*.doc)|*.doc|PDF files (*.pdf)|*.pdf|All files (*.*)|*.*", wx.FD_OPEN | wx.FD_CHANGE_DIR)
        if dialog.ShowModal() == wx.ID_OK:
            path.SetValue(str(dialog.GetPath()))
        dialog.Destroy()