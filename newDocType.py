import wx 

class NewDocType(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(NewDocType, self).__init__(*args, **kwargs) 
        
        # Add a panel so it looks correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)
 
        labelType = wx.StaticText(self.panel, wx.ID_ANY, 'Tip')
        self._docType = wx.TextCtrl(self.panel, wx.ID_ANY, '')
 
        labelDescription = wx.StaticText(self.panel, wx.ID_ANY, 'Descriere')
        self._description = wx.TextCtrl(self.panel, wx.ID_ANY, '')
 
        okBtn = wx.Button(self.panel, wx.ID_OK, 'OK')        
        cancelBtn = wx.Button(self.panel, wx.ID_CANCEL, 'Cancel')
 
        topSizer        = wx.BoxSizer(wx.VERTICAL)
        inputOneSizer   = wx.BoxSizer(wx.HORIZONTAL)
        inputTwoSizer   = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer        = wx.BoxSizer(wx.HORIZONTAL)
 
        inputOneSizer.Add(labelType, 0, wx.ALL, 5)
        inputOneSizer.Add(self._docType, 1, wx.ALL|wx.EXPAND, 5)
 
        inputTwoSizer.Add(labelDescription, 0, wx.ALL, 5)
        inputTwoSizer.Add(self._description, 1, wx.ALL|wx.EXPAND, 5)
 
        btnSizer.Add(okBtn, 0, wx.ALL, 5)
        btnSizer.Add(cancelBtn, 0, wx.ALL, 5)
 
        topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(inputOneSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(inputTwoSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btnSizer, 0, wx.ALL|wx.CENTER, 5)
 
        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)

    def GetDocumentType(self):
        return self._docType.GetValue()
		
    def GetDocumentDescription(self):
        return self._description.GetValue()