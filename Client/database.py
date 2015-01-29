__author__ = 'Costin'

import pyodbc
import wx

#connString = 'DRIVER={SQL Server};SERVER=LAPTOP\SQLSERVEREXPRESS;DATABASE=NumereDB;UID=sa;PWD=alibaba'
connString = 'DSN=NumereDB;Trusted_Connection=yes'

def TestLogin(username, password):
    try:
        conn = pyodbc.connect(connString, autocommit=True)
        curs = conn.cursor()
        curs.execute('SELECT COUNT(*) AS Status FROM USERS WHERE username = ? and password = ?', username, password)
        row = curs.fetchone()
        conn.close()
        status = False if row.Status < 1 else True
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
    return status