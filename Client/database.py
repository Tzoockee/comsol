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

def GetUserFullName(username):
    try:
        conn = pyodbc.connect(connString, autocommit=True)
        curs = conn.cursor()
        curs.execute('SELECT firstname, lastname FROM USERS WHERE username = ?', username)
        row = curs.fetchone()
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
    return row.firstname + ' ' + row.lastname

def GetDocumentTypes():
    try:
        conn = pyodbc.connect(connString, autocommit=True)
        curs = conn.cursor()
        curs.execute('SELECT docType FROM DocType')
        rows = curs.fetchall()
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
    return rows

def GetUserId(username):
    try:
        conn = pyodbc.connect(connString, autocommit=True)
        curs = conn.cursor()
        curs.execute('SELECT id FROM Users WHERE username = ?', username)
        row = curs.fetchone()
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
    return row.id

def GetDocTypeId(docType):
    try:
        conn = pyodbc.connect(connString, autocommit=True)
        curs = conn.cursor()
        curs.execute('SELECT id FROM DocType WHERE docType = ?', docType)
        row = curs.fetchone()
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
    return row.id

def AddDocument(authUser, docType, userDate, lastName, firstName, filePath, description):
    userId = GetUserId(authUser)
    docTypeId = GetDocTypeId(docType)
    try:
        conn = pyodbc.connect(connString, autocommit=True)
        curs = conn.cursor()
        curs.execute('INSERT INTO Documents(user_id, doctype_id, user_date, file_path, first_name, last_name, description) VALUES (?, ?, ?, ?, ?, ?, ?)', userId, docTypeId, userDate, filePath, firstName, lastName, description)
        curs.execute('SELECT @@IDENTITY As newNumber')
        row = curs.fetchone()
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
    return str(row.newNumber) + ' - ' + userDate