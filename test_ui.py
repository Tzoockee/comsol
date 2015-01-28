import wx 
import newUser
import login
import changePass
import sys
import shutil

username = ''

class MainFrame(wx.Frame):

	def __init__(self, *args, **kwargs):
		super(MainFrame, self).__init__(*args, **kwargs) 
		
		self.panel = wx.Panel(self, wx.ID_ANY)

		newUser = wx.Button(self.panel, label='Utilizator nou')
		self.Bind(wx.EVT_BUTTON, self.OnCls, newUser)

		changePass = wx.Button(self.panel, label='Schimbare parola')
		self.Bind(wx.EVT_BUTTON, self.OnChangePass, changePass)

		topSizer = wx.BoxSizer(wx.VERTICAL)
		topSizer.Add(wx.StaticText(self.panel, wx.ID_ANY, username), 0, wx.ALL|wx.EXPAND, 5)
		topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
		topSizer.Add(newUser, 0, wx.ALL|wx.EXPAND, 5)
		topSizer.Add(changePass, 0, wx.ALL|wx.EXPAND, 5)

		self.panel.SetSizer(topSizer)
		topSizer.Fit(self)

	def OnCls(self, event):
		subframe = newUser.NewUser(None, -1, 'Utilizator nou')
		ret = subframe.ShowModal()		
		if ret == wx.ID_OK:
			print subframe.GetName()
		else:
			print 'CANCEL'
		subframe.Destroy()

	def OnChangePass(self, event):
		changePassDlg = changePass.ChangePass(None, -1, 'Schimbare Parola')
		ret = changePassDlg.ShowModal()
		if ret == wx.ID_OK:
			print changePassDlg.GetOldPassword() + ' ' + changePassDlg.GetNewPassword()
		else:
			print 'CANCEL'
		changePassDlg.Destroy()

app = wx.App()

#Login section
loginDlg = login.Login(None, -1, 'Autentificare')
ret = loginDlg.ShowModal()
if ret == wx.ID_OK:
	print loginDlg.GetUserName() + ' ' + loginDlg.GetPassword()
	username = loginDlg.GetUserName()
else:
	loginDlg.Destroy()
	sys.exit()
	
loginDlg.Destroy()
		
#main frame
frame = MainFrame(None, -1, 'Test UI')
frame.Show()
app.MainLoop()