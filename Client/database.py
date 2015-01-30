__author__ = 'Costin'

import pyodbc
import wx
import client_cfg

def Connection():
    conn = pyodbc.connect(client_cfg.DB_Connection, autocommit=True)
    return conn

def TestLogin(username, password):
    try:
        conn = Connection()
        curs = conn.cursor()
        curs.execute('SELECT COUNT(*) AS Status FROM USERS WHERE username = ? and password = ?', username, password)
        row = curs.fetchone()
        conn.close()
        status = False if row.Status < 1 else True
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
    return status

def ChangePassword(username, password):
    userId = GetUserId(username)
    try:
        conn = Connection()
        curs = conn.cursor()
        curs.execute('UPDATE Users SET password = ? WHERE ID = ?', password, userId)
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)

def GetUserFullName(username):
    try:
        conn = Connection()
        curs = conn.cursor()
        curs.execute('SELECT firstname, lastname FROM USERS WHERE username = ?', username)
        row = curs.fetchone()
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
    return row.firstname + ' ' + row.lastname

def GetDocumentTypes():
    try:
        conn = Connection()
        curs = conn.cursor()
        curs.execute('SELECT docType FROM DocType')
        rows = curs.fetchall()
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
    return rows

def GetUserId(username):
    try:
        conn = Connection()
        curs = conn.cursor()
        curs.execute('SELECT id FROM Users WHERE username = ?', username)
        row = curs.fetchone()
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
    return row.id

def GetDocTypeId(docType):
    try:
        conn = Connection()
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
        conn = Connection()
        curs = conn.cursor()
        curs.execute('SET DATEFORMAT dmy')
        curs.execute('INSERT INTO Documents(user_id, doctype_id, user_date, file_path, first_name, last_name, description) VALUES (?, ?, ?, ?, ?, ?, ?)', userId, docTypeId, userDate, filePath, firstName, lastName, description)
        curs.execute('SELECT @@IDENTITY As newNumber')
        row = curs.fetchone()
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
    return str(row.newNumber) + ' - ' + userDate

def GetDocument(number):
    try:
        conn = Connection()
        curs = conn.cursor()
        curs.execute('SELECT file_path FROM Documents WHERE ID = ?', number)
        row = curs.fetchone()
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
    return row.file_path

def GetReport(authUser, docType, dateFrom, dateTo):
    userId = GetUserId(authUser)
    docTypeId = GetDocTypeId(docType)
    try:        
        conn = Connection()
        curs = conn.cursor()
        curs.execute('SET DATEFORMAT dmy')
        curs.execute("""SELECT 
                            D.id As Numar,
                            D.user_date As Data,
                            DT.docType As Tip,                            
                            D.last_name + ' ' + D.first_name As Solicitant
                        FROM 
                            Documents D INNER JOIN DocType DT ON D.doctype_id = DT.ID
                        WHERE
                            d.docType_id = ? AND D.user_id = ? AND D.user_date >= ? AND d.user_date <= ?""", docTypeId, userId, dateFrom, dateTo)
        rows = curs.fetchall()
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
    return rows