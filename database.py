__author__ = 'Costin'

import pyodbc
import wx

connString = 'DRIVER={SQL Server};SERVER=LAPTOP\SQLSERVEREXPRESS;DATABASE=NumereDB;UID=sa;PWD=alibaba'

def AddNewUser(username, firstname, lastname):
    try:
        conn = pyodbc.connect(connString, autocommit=True)
        curs = conn.cursor()
        curs.execute('INSERT INTO USERS(username, firstname, lastname, password) VALUES(?, ?, ?, ?)', username, firstname, lastname, username)
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)

def DeleteUser(username):
    try:
        conn = pyodbc.connect(connString, autocommit=True)
        curs = conn.cursor()
        curs.execute('DELETE FROM USERS WHERE username = ''?''', username)
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)