import wx 

class ChangePass(wx.Dialog):
	def __init__(self, *args, **kwargs):
		super(ChangePass, self).__init__(*args, **kwargs) 
		
		# Add a panel so it looks correct on all platforms
		self.panel = wx.Panel(self, wx.ID_ANY)
 
		labelOldPass = wx.StaticText(self.panel, wx.ID_ANY, 'Parola veche')
		self._oldPass = wx.TextCtrl(self.panel, wx.ID_ANY, '', style=wx.TE_PASSWORD)
 
		labelNewPass1 = wx.StaticText(self.panel, wx.ID_ANY, 'Parola noua')
		self._newPass1 = wx.TextCtrl(self.panel, wx.ID_ANY, '', style=wx.TE_PASSWORD)
 
		labelNewPass2 = wx.StaticText(self.panel, wx.ID_ANY, 'Parola noua')
		self._newPass2 = wx.TextCtrl(self.panel, wx.ID_ANY, '', style=wx.TE_PASSWORD)
 
		okBtn = wx.Button(self.panel, wx.ID_OK, 'OK')		
		cancelBtn = wx.Button(self.panel, wx.ID_CANCEL, 'Cancel')
 
		self.Bind(wx.EVT_BUTTON, self.OnOK, okBtn)
 
		topSizer		= wx.BoxSizer(wx.VERTICAL)
		inputOneSizer   = wx.BoxSizer(wx.HORIZONTAL)
		inputTwoSizer   = wx.BoxSizer(wx.HORIZONTAL)
		inputThreeSizer = wx.BoxSizer(wx.HORIZONTAL)
		btnSizer		= wx.BoxSizer(wx.HORIZONTAL)
 
		inputOneSizer.Add(labelOldPass, 0, wx.ALL, 5)
		inputOneSizer.Add(self._oldPass, 1, wx.ALL|wx.EXPAND, 5)
 
		inputTwoSizer.Add(labelNewPass1, 0, wx.ALL, 5)
		inputTwoSizer.Add(self._newPass1, 1, wx.ALL|wx.EXPAND, 5)
 
		inputThreeSizer.Add(labelNewPass2, 0, wx.ALL, 5)
		inputThreeSizer.Add(self._newPass2, 1, wx.ALL|wx.EXPAND, 5)
 
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
	
	def GetOldPassword(self):
		return self._oldPass.GetValue()
		
	def GetNewPassword(self):
		return self._newPass1.GetValue()
	
	def OnOK(self, event):
		if self._newPass1.GetValue() != self._newPass2.GetValue() or self._newPass1.GetValue() == '' :
			print 'TODO: error'
		else:
			event.Skip()