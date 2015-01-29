import wx 

class Login(wx.Dialog):
	def __init__(self, *args, **kwargs):
		super(Login, self).__init__(*args, **kwargs) 
		
		# Add a panel so it looks correct on all platforms
		self.panel = wx.Panel(self, wx.ID_ANY)
 
		labelUser = wx.StaticText(self.panel, wx.ID_ANY, 'Utilizator')
		self._user = wx.TextCtrl(self.panel, wx.ID_ANY, '')
 
		labelPassword = wx.StaticText(self.panel, wx.ID_ANY, 'Parola')
		self._password = wx.TextCtrl(self.panel, wx.ID_ANY, '', style=wx.TE_PASSWORD)
		
		okBtn = wx.Button(self.panel, wx.ID_OK, 'OK')		
		cancelBtn = wx.Button(self.panel, wx.ID_CANCEL, 'Cancel')		
		
		topSizer		= wx.BoxSizer(wx.VERTICAL)
		inputOneSizer   = wx.BoxSizer(wx.HORIZONTAL)
		inputTwoSizer   = wx.BoxSizer(wx.HORIZONTAL)
		btnSizer		= wx.BoxSizer(wx.HORIZONTAL)
		
		inputOneSizer.Add(labelUser, 0, wx.ALL, 5)
		inputOneSizer.Add(self._user, 1, wx.ALL|wx.EXPAND, 5)
 
		inputTwoSizer.Add(labelPassword, 0, wx.ALL, 5)
		inputTwoSizer.Add(self._password, 1, wx.ALL|wx.EXPAND, 5)
		
		btnSizer.Add(okBtn, 0, wx.ALL, 5)
		btnSizer.Add(cancelBtn, 0, wx.ALL, 5)
		
		topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
		topSizer.Add(inputOneSizer, 0, wx.ALL|wx.EXPAND, 5)
		topSizer.Add(inputTwoSizer, 0, wx.ALL|wx.EXPAND, 5)
		topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
		topSizer.Add(btnSizer, 0, wx.ALL|wx.CENTER, 5)
		
		self.panel.SetSizer(topSizer)
		topSizer.Fit(self)        
		okBtn.SetDefault()
		self._user.SetFocus()
		
	def GetUserName(self):
		return self._user.GetValue()
		
	def GetPassword(self):
		return self._password.GetValue()
		
		